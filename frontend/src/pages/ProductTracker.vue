<!-- filepath: /home/sergio/coupang-rank-tracker/frontend/src/pages/ProductTracker.vue -->
<template>
  <q-page padding>
    <div class="row q-col-gutter-md">
      <!-- 상품 추가 폼 -->
      <div class="col-12 col-md-6">
        <q-card>
          <q-card-section>
            <div class="text-h6">상품 추가</div>
          </q-card-section>

          <q-card-section>
            <q-form @submit="onSubmit" class="q-gutter-md">
              <q-input
                v-model="form.url"
                label="상품 URL"
                :rules="[val => !!val || 'URL을 입력해주세요']"
              />
              <q-input
                v-model="form.name"
                label="상품 이름"
                :rules="[val => !!val || '상품 이름을 입력해주세요']"
              />
              <div class="row q-col-gutter-sm items-center">
                <div class="col">
                  <q-input
                    v-model="newKeyword"
                    label="검색 키워드"
                    @keyup.enter="addKeyword"
                  />
                </div>
                <div class="col-auto">
                  <q-btn
                    color="primary"
                    icon="add"
                    @click="addKeyword"
                    :disable="!newKeyword"
                  />
                </div>
              </div>

              <!-- 키워드 칩 목록 -->
              <div class="q-gutter-sm">
                <q-chip
                  v-for="(keyword, index) in form.keywords"
                  :key="index"
                  removable
                  @remove="removeKeyword(index)"
                >
                  {{ keyword }}
                </q-chip>
              </div>

              <q-btn
                type="submit"
                color="primary"
                label="추가"
                :loading="loading"
              />
            </q-form>
          </q-card-section>
          <q-card-section v-if="rankResult">
            <div v-if="rankResult.rank !== null">
              <q-banner class="bg-green-2 text-green-10">
                {{ form.keywords[0] || '키워드' }} 검색 결과<br>
                <b>{{ form.url }}</b><br>
                <span>→ {{ rankResult.page }}페이지, {{ rankResult.rank }}번째에 노출됩니다.</span>
              </q-banner>
              <div v-if="rankResult.screenshots && rankResult.screenshots.length">
                <div class="q-mt-md">화면 캡처:</div>
                <div class="row q-col-gutter-md">
                  <div v-for="(shot, idx) in rankResult.screenshots" :key="idx" class="col-auto">
                    <q-img :src="getScreenshotUrl(shot)" style="max-width:200px;max-height:300px;" :alt="`캡처 ${idx+1}`" />
                    <q-btn flat color="primary" icon="download" :href="getScreenshotUrl(shot)" :download="`capture_${idx+1}.png`" label="다운로드" class="q-mt-xs" />
                  </div>
                </div>
              </div>
            </div>
            <div v-else>
              <q-banner class="bg-red-2 text-red-10">
                {{ rankResult.message || '상품이 검색 결과에 없습니다.' }}
              </q-banner>
            </div>
          </q-card-section>
        </q-card>
      </div>

      <!-- 상품 목록 -->
      <div class="col-12">
        <q-card>
          <q-card-section>
            <div class="text-h6">등록된 상품</div>
          </q-card-section>

          <q-card-section>
            <q-list>
              <q-expansion-item
                v-for="product in products"
                :key="product.id"
                :label="product.name"
                :caption="product.url"
              >
                <q-card>
                  <q-card-section>
                    <div class="row items-center q-gutter-sm">
                      <q-chip
                        v-for="keyword in product.keywords"
                        :key="keyword.id"
                        size="sm"
                      >
                        {{ keyword.keyword }}
                      </q-chip>
                      <q-btn
                        color="primary"
                        icon="refresh"
                        label="순위 체크"
                        @click="checkRanks(product.id)"
                        :loading="checking[product.id]"
                      />
                    </div>
                  </q-card-section>

                  <!-- 순위 결과 표시 -->
                  <q-card-section v-if="(rankings[product.id] || []).length > 0">
                    <q-table
                      :rows="rankings[product.id] || []"
                      :columns="[
                        { name: 'keyword', label: '키워드', field: 'keyword' },
                        { name: 'rank', label: '순위', field: 'rank' },
                        { name: 'checked_at', label: '체크 시간', field: 'checked_at' }
                      ]"
                      row-key="keyword"
                      dense
                    />
                  </q-card-section>
                </q-card>
              </q-expansion-item>
            </q-list>
          </q-card-section>
        </q-card>
      </div>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import type { Ref } from 'vue';
import { ref } from 'vue'
import { api } from 'boot/axios'

const form = ref({
  url: '',
  name: '',
  keywords: [] as string[]
})

const products : Ref<{id: string, name : string, url : string, keywords : { id : string, keyword: string }[]}[]>= ref([])
const loading = ref(false)
const newKeyword = ref('')

const addKeyword = () => {
  if (newKeyword.value && !form.value.keywords.includes(newKeyword.value)) {
    form.value.keywords.push(newKeyword.value)
    newKeyword.value = ''
  }
}

const removeKeyword = (index: number) => {
  form.value.keywords.splice(index, 1)
}

interface RankResult {
  rank: number|null,
  page: number|null,
  message?: string,
  screenshots?: string[]
}
const rankResult = ref<RankResult|null>(null)

const onSubmit = async () => {
  try {
    loading.value = true
    rankResult.value = null; // 기존 검색 결과 제거
    const { data } = await api.post('/rank', {
      search_keyword: form.value.keywords[0] || '모기장',
      product_url: form.value.url,
      max_pages: 3
    })
    rankResult.value = data
  } catch (error) {
    console.error(error)
    rankResult.value = { rank: null, page: null, message: '에러가 발생했습니다.' }
  } finally {
    loading.value = false
  }
}

// 캡처 이미지 파일 경로를 API URL로 변환 (백엔드에서 정적 파일로 제공해야 함)
function getScreenshotUrl(path: string) {
  if (!path) return ''
  // /tmp/로 시작하면 /static/로 변환
  if (path.startsWith('/tmp/')) {
    return `${api.defaults.baseURL || ''}/static/${path.slice(5)}`
  }
  // /로 시작하면 /static/로 변환
  if (path.startsWith('/')) {
    return `${api.defaults.baseURL || ''}/static${path}`
  }
  return path
}

const checking = ref<Record<string, boolean>>({})
const rankings = ref<Record<string, Array<{keyword: string, rank: number, checked_at: string}>>>({})

const checkRanks = async (productId: string) => {
  try {
    checking.value[productId] = true
    const { data } = await api.post(`/rank/${productId}/check-ranks`)

    // 태스크 결과 폴링
    for (const task of data.tasks) {
      let status = 'PENDING'
      while (status === 'PENDING') {
        await new Promise(resolve => setTimeout(resolve, 1000))
        const { data: taskResult } = await api.get(`/tasks/${task.task_id}`)
        status = taskResult.status
        if (status === 'SUCCESS') {
          // 순위 결과 저장
          if (!rankings.value[productId]) {
            rankings.value[productId] = []
          }
          rankings.value[productId].push({
            keyword: task.keyword,
            rank: taskResult.result.rank,
            checked_at: new Date().toLocaleString()
          })
        }
      }
    }
  } catch (error) {
    console.error('Error:', error)
  } finally {
    checking.value[productId] = false
  }
}
</script>
