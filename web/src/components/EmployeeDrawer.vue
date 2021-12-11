<script setup lang="ts">
// @ts-ignore
import {
  NForm,
  NFormItemGi,
  NGrid,
  NH2,
  NInput,
  NDatePicker,
  NDrawer,
  NDrawerContent,
  NSelect,
  NUpload,
  NButton,
  NInputNumber,
  useLoadingBar,
  useNotification,
} from 'naive-ui'
import type { UploadFileInfo } from 'naive-ui'
import type { PropType } from 'vue'
import type { SelectOption, EmployeeView } from '~/types'
import type { DrawerType } from '~/stores/drawer'
import { useDrawerStore } from '~/stores/drawer'
import { FormModelType, useFormStore } from '~/stores/form'

type CreateEmployeeRequest = {
  email: string
  username: string
  password: string
  phone_number: string
  first_name: string
  last_name: string
  gender: string
  dob: string
  salary: number
  role: string
  start_at: string
  end_at?: string
  avatar_image?: string
  address?: {
    city: string
    line1: string
    line2?: string
    state: string
    country: string
    postal_code: string
  }
  department?: string
}

type UpdateEmployeeRequest = {
  email?: string
  username?: string
  password?: string
  phone_number?: string
  first_name?: string
  last_name?: string
  gender?: string
  dob?: string
  salary?: number
  role?: string
  start_at?: string
  end_at?: string
  avatar_image?: string
  address?: {
    city: string
    line1: string
    line2?: string
    state: string
    country: string
    postal_code: string
  }
  department?: string
}

const props = defineProps({
  type: { required: true, type: String as PropType<DrawerType> },
  refetch: { type: Function as PropType<() => void> },
  departmentOptions: { required: true, type: Array as PropType<SelectOption[]> },
  genderOptions: { required: true, type: Array as PropType<SelectOption[]> },
  roleOptions: { required: true, type: Array as PropType<SelectOption[]> },
})

const loadingBar = useLoadingBar()
const notification = useNotification()
const drawer = useDrawerStore()
const form = useFormStore()

const getBase64 = (file: File): Promise<string> => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader()
    reader.readAsDataURL(file)
    reader.onload = () => resolve(reader.result as string)
    reader.onerror = error => reject(error)
  })
}

const updateAvatarImage = async({ file }: { file: UploadFileInfo }) => {
  if (!file.file) return
  form.setFormModel('employee', { ...form.formModel.employee, user: { ...(form.formModel.employee.user as Record<string, unknown>), avatar_image: await getBase64(file.file) } })
}

const closeDrawer = () => drawer.setDrawerOpen(props.type, false)

const mapToCreateEmployeeRequest = ({ user, department, address, ...employee }: FormModelType['employee']): CreateEmployeeRequest => {
  if (!user.dob || !employee.salary || !employee.startAt) throw new Error('Required fields of CreateEmployeeRequest are null')
  return {
    email: user.email,
    username: user.username,
    // @ts-ignore
    password_hash: 'randomPassword',
    password: 'randomPassword',
    phone_number: user.phone_number,
    first_name: user.first_name,
    last_name: user.last_name,
    gender: user.gender,
    dob: new Date(user.dob).toISOString().split('T')[0],
    salary: employee.salary,
    role: employee.role,
    start_at: new Date(employee.startAt).toISOString().split('T')[0],
    end_at: employee.endAt ? new Date(employee.endAt).toISOString().split('T')[0] : undefined,
    avatar_image: user.avatar_image?.length === 0 ? undefined : user.avatar_image,
    address,
    department: department.name !== '' ? department.name : undefined,
  }
}

const mapToUpdateEmployeeRequest = ({ user, department, address, ...employee }: FormModelType['employee']): UpdateEmployeeRequest => {
  const res = {
    username: user.username,
    phone_number: user.phone_number,
    first_name: user.first_name,
    last_name: user.last_name,
    gender: user.gender,
    dob: user.dob ? new Date(user.dob).toISOString().split('T')[0] : undefined,
    salary: employee.salary ? employee.salary : undefined,
    role: employee.role,
    start_at: employee.startAt ? new Date(employee.startAt).toISOString().split('T')[0] : undefined,
    end_at: employee.endAt ? new Date(employee.endAt).toISOString().split('T')[0] : undefined,
    avatar_image: user.avatar_image?.length === 0 ? undefined : user.avatar_image,
    address: {
      city: address.city,
      state: address.state,
      postal_code: address.postal_code,
      country: address.country,
      line1: address.line1,
      line2: address.line2 ? address.line2 : undefined,
    },
    department: department.name !== '' ? department.name : undefined,
  }
  if (!employee.endAt) delete res.end_at
  if (!address.line2) delete res.address.line2
  if (user.avatar_image?.length === 0) delete res.avatar_image
  return res
}

const createEmployee = (employee: FormModelType['employee']) => {
  loadingBar.start()
  const { onFetchError, onFetchResponse, data } = useFetch<EmployeeView>(`
    ${import.meta.env.VITE_SERVER_URL}/employee`,
  {
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(mapToCreateEmployeeRequest(employee)),
  },
  {},
  ).post().json<EmployeeView>()
  onFetchError((error) => {
    console.error(error)
    loadingBar.error()
    notification.error({ title: 'An error occurred', meta: 'Unable to create employee' })
  })
  onFetchResponse(() => {
    if (props.refetch) props.refetch()
    loadingBar.finish()
    notification.success({ title: 'Successfully created', meta: `Employee with username ${(form.formModel.employee.user as unknown as {username: string}).username} is created` })
    drawer.setDrawerOpen('create', false)
  })
}

const updateEmployee = (employee: FormModelType['employee']) => {
  loadingBar.start()
  const { onFetchError, onFetchResponse, data } = useFetch<EmployeeView>(`
    ${import.meta.env.VITE_SERVER_URL}/employee/${employee.user.username}`,
  {
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(mapToUpdateEmployeeRequest(employee)),
  },
  {},
  ).put().json<EmployeeView>()
  onFetchError((error) => {
    console.error(error)
    loadingBar.error()
    notification.error({ title: 'An error occurred', meta: 'Unable to update employee' })
  })
  onFetchResponse(() => {
    if (props.refetch) props.refetch()
    loadingBar.finish()
    notification.success({ title: 'Successfully updated', meta: `Employee with username ${(form.formModel.employee.user as unknown as {username: string}).username} is updated` })
    drawer.setDrawerOpen('edit', false)
  })
}

const handleActionButton = () => props.type === 'create' ? createEmployee(form.formModel.employee as FormModelType['employee']) : updateEmployee(form.formModel.employee as FormModelType['employee'])
</script>

<template>
  <n-drawer
    :show="type === 'create' ? drawer.drawerOpen.create : drawer.drawerOpen.edit"
    :width="460"
    :on-mask-click="closeDrawer"
  >
    <n-drawer-content>
      <n-form size="small" :model="form.formModel.employee">
        <n-grid :span="24" :x-gap="4">
          <n-form-item-gi :span="24">
            <n-h2 class="mb-0">
              User
            </n-h2>
          </n-form-item-gi>
          <n-form-item-gi :span="12" label="First Name" path="form.formModel.employee.user.first_name">
            <n-input v-model:value="form.formModel.employee.user.first_name" placeholder="First Name" />
          </n-form-item-gi>
          <n-form-item-gi :span="12" label="Last Name" path="form.formModel.employee.user.last_name">
            <n-input v-model:value="form.formModel.employee.user.last_name" placeholder="Last Name" />
          </n-form-item-gi>
          <n-form-item-gi :span="12" label="Username" path="form.formModel.employee.user.username">
            <n-input
              v-model:value="form.formModel.employee.user.username"
              :disabled="props.type === 'edit'"
              placeholder="Username"
            />
          </n-form-item-gi>
          <n-form-item-gi :span="12" label="Email" path="form.formModel.employee.user.email">
            <n-input
              v-model:value="form.formModel.employee.user.email"
              :disabled="props.type === 'edit'"
              placeholder="Email"
            />
          </n-form-item-gi>
          <n-form-item-gi
            :span="12"
            label="Phone Number"
            path="form.formModel.employee.user.phone_number"
          >
            <n-input
              v-model:value="form.formModel.employee.user.phone_number"
              placeholder="Phone Number"
            />
          </n-form-item-gi>
          <n-form-item-gi :span="12" label="Date of Birth" path="form.formModel.employee.user.dob">
            <n-date-picker v-model:value="form.formModel.employee.user.dob" type="date" />
          </n-form-item-gi>
          <n-form-item-gi :span="24" label="Gender" path="form.formModel.employee.user.gender">
            <n-select
              v-model:value="form.formModel.employee.user.gender"
              placeholder="Gender"
              :options="genderOptions"
            />
          </n-form-item-gi>
          <n-form-item-gi :span="24" label="Avatar" path="form.formModel.employee.user.avatar_image">
            <n-upload list-type="image-card" :max="1" :file-list-style="{ display: 'flex' }" :on-change="updateAvatarImage" />
          </n-form-item-gi>
          <n-form-item-gi :span="24">
            <n-h2 class="mb-0">
              Employee
            </n-h2>
          </n-form-item-gi>
          <n-form-item-gi :span="24" label="Department" path="form.formModel.employee.department.name">
            <n-select
              v-model:value="form.formModel.employee.department.name"
              placeholder="Department"
              :options="departmentOptions"
            />
          </n-form-item-gi>
          <n-form-item-gi :span="12" label="Start At" path="form.formModel.employee.startAt">
            <n-date-picker v-model:value="form.formModel.employee.startAt" type="date" />
          </n-form-item-gi>
          <n-form-item-gi :span="12" label="End At" path="form.formModel.employee.endAt">
            <n-date-picker v-model:value="form.formModel.employee.endAt" type="date" />
          </n-form-item-gi>
          <n-form-item-gi :span="12" label="Role" path="form.formModel.employee.role">
            <n-select
              v-model:value="form.formModel.employee.role"
              placeholder="Role"
              :options="roleOptions"
            />
          </n-form-item-gi>
          <n-form-item-gi :span="12" label="Salary" path="form.formModel.employee.salary">
            <n-input-number v-model:value="form.formModel.employee.salary" placeholder="Salary">
              <template #prefix>
                RM
              </template>
            </n-input-number>
          </n-form-item-gi>
          <n-form-item-gi :span="24" :style="{ padding: 0 }">
            <n-h2 class="mb-0">
              Address
            </n-h2>
          </n-form-item-gi>
          <n-form-item-gi :span="24" label="Address Line 1" path="form.formModel.employee.address.line1">
            <n-input v-model:value="form.formModel.employee.address.line1" placeholder="Address Line 1" />
          </n-form-item-gi>
          <n-form-item-gi :span="24" label="Address Line 2" path="form.formModel.employee.address.line2">
            <n-input v-model:value="form.formModel.employee.address.line2" placeholder="Address Line 2" />
          </n-form-item-gi>
          <n-form-item-gi :span="12" label="City" path="form.formModel.employee.address.city">
            <n-input v-model:value="form.formModel.employee.address.city" placeholder="City" />
          </n-form-item-gi>
          <n-form-item-gi :span="12" label="State" path="form.formModel.employee.address.state">
            <n-input v-model:value="form.formModel.employee.address.state" placeholder="State" />
          </n-form-item-gi>
          <n-form-item-gi
            :span="12"
            label="Postal Code"
            path="form.formModel.employee.address.postal_code"
          >
            <n-input
              v-model:value="form.formModel.employee.address.postal_code"
              placeholder="Postal Code"
            />
          </n-form-item-gi>
          <n-form-item-gi :span="12" label="Country" path="form.formModel.employee.address.country">
            <n-input v-model:value="form.formModel.employee.address.country" placeholder="Country" />
          </n-form-item-gi>
        </n-grid>
      </n-form>
      <template #footer>
        <n-button ghost type="error" class="mr-2" @click="closeDrawer">
          Cancel
        </n-button>
        <n-button type="success" @click="handleActionButton">
          {{ type === 'create' ? 'Create' : 'Apply' }}
        </n-button>
      </template>
    </n-drawer-content>
  </n-drawer>
</template>
