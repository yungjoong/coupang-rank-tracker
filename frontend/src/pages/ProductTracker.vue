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
import { ref, onMounted } from 'vue'
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

const onSubmit = async () => {
  try {
    loading.value = true
    // 상품 추가
    const { data: product } = await api.post('/products', {
      url: form.value.url,
      name: form.value.name
    })

    // 키워드 추가
    for (const keyword of form.value.keywords) {
      await api.post(`/products/${product.id}/keywords`, {
        keyword
      })
    }

    // 폼 초기화
    form.value = {
      url: '',
      name: '',
      keywords: []
    }

    // 목록 새로고침
    await fetchProducts()
  } catch (error) {
    console.error('Error:', error)
  } finally {
    loading.value = false
  }
}

const fetchProducts = async () => {
  try {
    const { data } = await api.get('/products')
    products.value = data
  } catch (error) {
    console.error('Error:', error)
  }
}

const checking = ref<Record<string, boolean>>({})
const rankings = ref<Record<string, Array<{keyword: string, rank: number, checked_at: string}>>>({})

const checkRanks = async (productId: string) => {
  try {
    checking.value[productId] = true
    const { data } = await api.post(`/products/${productId}/check-ranks`)

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

onMounted(async () => {
  await fetchProducts()
})
</script>
