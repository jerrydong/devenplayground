<script setup lang="ts">
import { ref } from 'vue';
import { Form, Input, Button, Select } from 'ant-design-vue';
import type { FormInstance } from 'ant-design-vue/es/form';
import type { SelectValue } from 'ant-design-vue/es/select';

interface Props {
  cityOptions: Array<{ id: number; name: string; }>;
  loading?: boolean;
}

const props = defineProps<Props>();
const emit = defineEmits<{
  (e: 'search', values: any): void;
  (e: 'reset'): void;
  (e: 'search-city', value: string): void;
  (e: 'load-more'): void;
}>();

const formRef = ref<FormInstance | null>(null);
interface FormState {
  name: string;
  age: number | undefined;
  address: string;
  city: string | undefined;
}

const modelRef = ref<FormState>({
  name: '',
  age: undefined,
  address: '',
  city: undefined,
});

const { resetFields, validate } = Form.useForm(modelRef);

const handleFinish = async () => {
  try {
    await validate();
    emit('search', modelRef.value);
  } catch (error) {
    console.error('Validation failed:', error);
  }
};

const handleReset = () => {
  resetFields();
  emit('reset');
};

const handleCityChange = (value: SelectValue) => {
  modelRef.value.city = value as string;
};
</script>

<template>
  <a-form
    ref="formRef"
    :model="modelRef"
    layout="inline"
    @finish="handleFinish"
    class="mb-4 p-4 bg-white rounded-lg shadow"
  >
    <a-form-item name="name" label="Name">
      <a-input v-model:value="modelRef.name" placeholder="Search by name" allow-clear />
    </a-form-item>
    <a-form-item name="age" label="Age">
      <a-input v-model:value="modelRef.age" placeholder="Search by age" type="number" allow-clear />
    </a-form-item>
    <a-form-item name="address" label="Address">
      <a-input v-model:value="modelRef.address" placeholder="Search by address" allow-clear />
    </a-form-item>
    <a-form-item name="city" label="City">
      <a-select
        placeholder="Select city"
        :style="{ width: '200px' }"
        show-search
        allow-clear
        :loading="loading"
        :filter-option="false"
        :options="cityOptions.map(city => ({
          value: city.name,
          label: city.name,
        }))"
        :not-found-content="loading ? 'Loading...' : null"
        @search="(value) => $emit('search-city', value)"
        @change="handleCityChange"
        @popup-scroll="(e: Event) => {
          const target = e.target as HTMLDivElement;
          if (
            !props.loading &&
            target.scrollTop + target.offsetHeight === target.scrollHeight
          ) {
            emit('load-more');
          }
        }"
      />
    </a-form-item>
    <a-form-item>
      <a-button type="primary" html-type="submit">
        Search
      </a-button>
    </a-form-item>
    <a-form-item>
      <a-button @click="handleReset">Reset</a-button>
    </a-form-item>
  </a-form>
</template>
