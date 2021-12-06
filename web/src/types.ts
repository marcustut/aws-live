import { ViteSSGContext } from 'vite-ssg'

export type UserModule = (ctx: ViteSSGContext) => void

export type Address = {
  address_id: number
  city: string
  country: string
  line1: string
  line2: string
  postal_code: string
  state: string
}

export type Department = {
  department_id: number
  name: string
  description: string
  created_at: string
  updated_at: string
}

export type User = {
  user_id: number
  username: string
  email: string
  first_name: string
  last_name: string
  dob: string
  gender: string
  phone_number: string
  avatar_url: string | null
  updated_at: string
  created_at: string
}

export type EmployeeView = {
  employee_id: number
  role: string
  salary: string // TODO: check why is it string
  user: User
  address: Address
  department: Department
  start_at: string
  end_at: string | null
  created_at: string
  updated_at: string
}
