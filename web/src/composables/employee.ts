import { ref } from 'vue'

export type EmployeeFormModel = {
  user: {
    first_name: string
    last_name: string
    username: string
    email: string
    dob: number | null
    gender: string
    phone_number: string
    avatar_image: string
    avatar_url: string
  }
  address: {
    city: string
    country: string
    line1: string
    line2: string
    postal_code: string
    state: string
  }
  department: {
    name: string
    description: string
    created_at: string
    updated_at: string
  }
  salary: number | null
  role: string
  startAt: number | null
  endAt: number | null
}

export const useEmployeeFormModel = () => ref<EmployeeFormModel>({
  user: {
    first_name: '',
    last_name: '',
    username: '',
    email: '',
    dob: null as number | null,
    gender: '',
    phone_number: '',
    avatar_image: '',
    avatar_url: '',
  },
  address: {
    city: '',
    country: '',
    line1: '',
    line2: '',
    postal_code: '',
    state: '',
  },
  department: {
    name: '',
    description: '',
    created_at: '',
    updated_at: '',
  },
  salary: null as number | null,
  role: '',
  startAt: null as number | null,
  endAt: null as number | null,
})
