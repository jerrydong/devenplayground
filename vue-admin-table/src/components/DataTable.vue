<script setup lang="ts">
import { ref, h, onMounted, watch } from 'vue'
import { debounce } from '../utils/debounce'
import { Button, message, Modal } from 'ant-design-vue'
import { DeleteOutlined } from '@ant-design/icons-vue'
import SearchForm from './SearchForm.vue'
import type { ColumnsType } from 'ant-design-vue/es/table'
import type { FilterDropdownProps } from 'ant-design-vue/es/table/interface'

interface DataType {
  key: string
  name: string
  age: number
  address: string
  city?: string
}

// Mock data
const initialData: DataType[] = [
  { key: '1', name: 'John Brown', age: 32, address: 'New York No. 1 Lake Park', city: 'New York' },
  { key: '2', name: 'Jim Green', age: 42, address: 'London No. 1 Lake Park', city: 'London' },
  { key: '3', name: 'Joe Black', age: 32, address: 'Sydney No. 1 Lake Park', city: 'Sydney' },
  { key: '4', name: 'Jim Red', age: 32, address: 'London No. 2 Lake Park', city: 'London' },
]

const data = ref<DataType[]>(initialData)
const searchInput = ref<HTMLInputElement | null>(null)
const cityOptions = ref<Array<{ id: number; name: string }>>([])
const loading = ref(false)
const searchParams = ref<{
  name?: string;
  age?: number;
  address?: string;
  city?: string;
}>({})

const currentPage = ref(1)
const searchTerm = ref('')
const hasMore = ref(true)
const pageSize = 10

const fetchCities = async (page: number, search: string) => {
  loading.value = true
  try {
    const response = await fetch(`/api/cities?page=${page}&pageSize=${pageSize}&search=${search}`)
    const result = await response.json()
    if (page === 1) {
      cityOptions.value = result.data
    } else {
      cityOptions.value = [...cityOptions.value, ...result.data]
    }
    currentPage.value = page
    hasMore.value = result.data.length === pageSize
  } catch (error) {
    message.error('Failed to fetch city options')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchCities(1, '')
})

// Update search results when searchParams changes
watch(searchParams, () => {
  handleFormSearch(searchParams.value)
})

const handleCitySearch = debounce((value: string) => {
  searchTerm.value = value
  cityOptions.value = []
  currentPage.value = 1
  hasMore.value = true
  fetchCities(1, value)
}, 300)

const handleLoadMore = () => {
  if (hasMore.value && !loading.value) {
    fetchCities(currentPage.value + 1, searchTerm.value)
  }
}

const handleFormSearch = (values: any) => {
  const searchValues = values === searchParams.value ? values : { ...values };
  loading.value = true;
  
  try {
    const filteredData = initialData.filter(item => {
      const nameMatch = !searchValues.name || item.name.toLowerCase().includes(searchValues.name.toLowerCase());
      const ageMatch = !searchValues.age || item.age === Number(searchValues.age);
      const addressMatch = !searchValues.address || item.address.toLowerCase().includes(searchValues.address.toLowerCase());
      const cityMatch = !searchValues.city || item.city === searchValues.city;
      
      return nameMatch && ageMatch && addressMatch && cityMatch;
    });
    
    if (filteredData.length === 0) {
      message.info('No records found matching the search criteria');
    }
    
    data.value = filteredData;
    if (values !== searchParams.value) {
      searchParams.value = searchValues;
    }
  } catch (error) {
    message.error('An error occurred while searching');
  } finally {
    loading.value = false;
  }
};

const handleFormReset = () => {
  searchParams.value = {};
  data.value = initialData;
};

const handleDelete = (key: string) => {
  Modal.confirm({
    title: 'Are you sure you want to delete this record?',
    okText: 'Yes',
    okType: 'danger',
    cancelText: 'No',
    onOk() {
      data.value = data.value.filter(item => item.key !== key)
      message.success('Record deleted successfully')
    },
  })
}

const getColumnSearchProps = (dataIndex: keyof DataType) => ({
  onFilter: (value: string | number | boolean, record: DataType) =>
    record[dataIndex]?.toString().toLowerCase().includes(value.toString().toLowerCase()) ?? false,
})

const columns: ColumnsType<DataType> = [
  {
    title: 'Name',
    dataIndex: 'name',
    key: 'name',
    ...getColumnSearchProps('name'),
  },
  {
    title: 'Age',
    dataIndex: 'age',
    key: 'age',
    ...getColumnSearchProps('age'),
  },
  {
    title: 'Address',
    dataIndex: 'address',
    key: 'address',
    ...getColumnSearchProps('address'),
  },
  {
    title: 'City',
    dataIndex: 'city',
    key: 'city',
    ...getColumnSearchProps('city'),
  },
  {
    title: 'Action',
    key: 'action',
    customRender: ({ record }: { record: DataType }) => {
      return h(Button, {
        type: 'link',
        danger: true,
        onClick: () => handleDelete(record.key)
      }, {
        default: () => [h(DeleteOutlined), ' Delete']
      })
    },
  },
]
</script>

<template>
  <div class="p-6 bg-white rounded-lg shadow">
    <h1 class="text-2xl font-bold mb-4">Data Table</h1>
    <SearchForm
      :cityOptions="cityOptions"
      :loading="loading"
      @search="handleFormSearch"
      @reset="handleFormReset"
      @search-city="handleCitySearch"
      @load-more="handleLoadMore"
    />
    <a-table
      :columns="columns"
      :data-source="data"
      :loading="loading"
      :pagination="{
        defaultPageSize: 5,
        showSizeChanger: true,
        showQuickJumper: true,
        total: data.length,
        showTotal: (total) => `Total ${total} items`,
      }"
    />
  </div>
</template>

<style scoped>
/* Component-specific styles */
</style>
