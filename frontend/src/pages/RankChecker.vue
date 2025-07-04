<template>
  <q-page padding>
    <q-card class="q-mx-auto" style="max-width: 500px;">
      <q-card-section>
        <div class="text-h6">쿠팡 상품 랭킹 체크</div>
      </q-card-section>
      <q-card-section>
        <q-form @submit="onSubmit" class="q-gutter-md">
          <q-input v-model="form.product_url" label="상품 URL" :rules="[val => !!val || 'URL을 입력하세요']" />
          <q-input v-model="form.search_keyword" label="검색어" :rules="[val => !!val || '검색어를 입력하세요']" />
          <q-input v-model.number="form.max_pages" label="최대 검색 페이지" type="number" min="1" max="10" />
          <q-btn type="submit" color="primary" label="순위 확인" :loading="loading" />
        </q-form>
      </q-card-section>
      <q-card-section v-if="result">
        <div v-if="result.rank !== null">
          <q-banner class="bg-green-2 text-green-10">
            {{ form.search_keyword }} 검색 결과<br>
            <b>{{ form.product_url }}</b><br>
            <span>→ {{ result.page }}페이지, {{ result.rank }}번째에 노출됩니다.</span>
          </q-banner>
        </div>
        <div v-else>
          <q-banner class="bg-red-2 text-red-10">
            상품이 검색 결과에 없습니다.
          </q-banner>
        </div>
      </q-card-section>
    </q-card>
  </q-page>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { api } from 'boot/axios'

const form = ref({
  product_url: '',
  search_keyword: '',
  max_pages: 5
})
const loading = ref(false)
const result = ref<{rank: number|null, page: number|null, message?: string}|null>(null)

const onSubmit = async () => {
  loading.value = true
  result.value = null
  try {
    const { data } = await api.post('/rank', form.value)
    result.value = data
  } catch (e) {
    let msg: string = '에러 발생';
    if (typeof e === 'string') msg = e;
    else if (e instanceof Error) msg = e.message;
    result.value = { rank: null, page: null, message: msg };
  } finally {
    loading.value = false
  }
}
</script>
