<script setup lang="ts">
import {
  NAvatar,
  NDataTable,
  NDrawer,
  NDrawerContent,
  NDescriptions,
  NDescriptionsItem,
  NP,
  NH2,
  NTag,
  NText,
  NSpace,
  NButton,
  NSelect,
  NInput,
  NInputNumber,
  NGrid,
  NIcon,
  NForm,
  NFormItemGi,
  NDatePicker,
  useLoadingBar,
  useNotification,
} from 'naive-ui'
import type { DataTableColumn } from 'naive-ui'
import { format, compareAsc } from 'date-fns'
import { Add, Edit, Delete } from '@vicons/carbon'
import type { EmployeeView } from '~/types'

const loadingBar = useLoadingBar()
const notification = useNotification()

const dataOpts = ref<{ cursor?: number; limit: number }>({ limit: 1000 })
const checkedRowKeys = ref<number[]>([])
const dateFormat = ref<string>('dd/MM/yyyy')
const editing = ref<{ employee: EmployeeView | null; isEditing: boolean }>({ employee: null, isEditing: false })
const editingFormRef = ref(null)
const addFormOpen = ref<boolean>(false)
const addFormRef = ref(null)

loadingBar.start()
const { data, onFetchError, onFetchResponse } = useFetch<EmployeeView[]>(`${import.meta.env.VITE_SERVER_URL}/employees?limit=${dataOpts.value.limit}`).get().json<EmployeeView[]>()

onFetchError(() => {
  loadingBar.error()
  notification.error({ title: 'An error occured', meta: 'Unable to fetch employees from server' })
})
onFetchResponse(() => loadingBar.finish())

const sortedData = computed(() => data.value ? data.value.sort((a, b) => a.employee_id - b.employee_id) : [])
const checkedData = computed(() => sortedData.value.length > 0 ? sortedData.value.filter(d => checkedRowKeys.value.includes(d.employee_id)) : [])
const departmentOptions = computed(() => [...new Set(sortedData.value.map(d => d.department.name))].map(n => ({ label: n, value: n })))

const pagination = {
  pageSize: 10,
}

const editEmployee = (employee: EmployeeView) => alert('Not implemented')

const deleteEmployee = (username: string) => {
  loadingBar.start()
  const { onFetchError, onFetchResponse } = useFetch<EmployeeView>(`${import.meta.env.VITE_SERVER_URL}/employee/${username}`).delete().json<EmployeeView>()
  onFetchError(() => {
    loadingBar.error()
    notification.error({ title: 'An error occured', meta: `Unable to delete employee - ${username}` })
  })
  onFetchResponse(() => {
    loadingBar.finish()
    notification.success({ title: 'Successfully deleted', meta: `Employee - ${username} had been deleted` })
  })
}

const bulkDeleteEmployee = () => {
  if (checkedData.value.length !== 0)
    checkedData.value.forEach(d => deleteEmployee(d.user.username))
  else
    notification.error({ title: 'No rows are selected', meta: 'Select at least one row to bulk delete' })
}

const genderOptions = ['Male', 'Female'].map(g => ({ label: g, value: g.toLowerCase() }))
const roleOptions = ['Admin', 'Manager', 'Runner', 'Cashier'].map(g => ({ label: g, value: g.toLowerCase() }))

const editingFormModel = ref({
  userValue: {
    first_name: '',
    last_name: '',
    username: '',
    email: '',
    dob: null as number | null,
    gender: '',
    phone_number: '',
    avatar_url: '',
  },

  departmentValue: {
    name: '',
  },

  addressValue: {
    city: '',
    country: '',
    line1: '',
    line2: '',
    postal_code: '',
    state: '',
  },

  salaryValue: null as number | null,
  roleValue: '',
  startAtValue: null as number | null,
  endAtValue: null as number | null,
})

watch(editing, () => {
  if (editing.value.employee) {
    const { user, address, department, ...employee } = editing.value.employee
    editingFormModel.value = {
      ...editingFormModel.value,
      userValue: {
        ...user,
        dob: new Date(user.dob).getTime(),
        avatar_url: user.avatar_url ?? '',
      },
      addressValue: address,
      departmentValue: { name: department.name },
      salaryValue: parseFloat(employee.salary),
      roleValue: employee.role,
      startAtValue: new Date(employee.start_at).getTime(),
      endAtValue: employee.end_at ? new Date(employee.end_at).getTime() : null,
    }
  }
})

const addFormModel = ref({
  userValue: {
    first_name: '',
    last_name: '',
    username: '',
    email: '',
    dob: null as number | null,
    gender: '',
    phone_number: '',
    avatar_url: '',
  },

  departmentValue: {
    name: '',
  },

  addressValue: {
    city: '',
    country: '',
    line1: '',
    line2: '',
    postal_code: '',
    state: '',
  },

  salaryValue: null as number | null,
  roleValue: '',
  startAtValue: null as number | null,
  endAtValue: null as number | null,
})

const columns: DataTableColumn<EmployeeView>[] = [
  {
    type: 'selection',
  },
  {
    type: 'expand',
    renderExpand: ({ user, address }) => {
      return h(
        NDescriptions,
        { labelPlacement: 'left', title: 'Details' },
        {
          default: () => [
            h(
              NDescriptionsItem,
              { label: 'Username' },
              { default: () => user.username },
            ),
            h(
              NDescriptionsItem,
              { label: 'Email' },
              { default: () => user.email },
            ),
            h(
              NDescriptionsItem,
              { label: 'Phone Number' },
              { default: () => user.phone_number },
            ),
            h(
              NDescriptionsItem,
              { label: 'Date Of Birth' },
              { default: () => user.dob },
            ),
            h(
              NDescriptionsItem,
              { label: 'Gender' },
              { default: () => user.gender },
            ),
            h(
              NDescriptionsItem,
              { label: 'Address' },
              { default: () => `${address.line1}, ${address.line2 ? `${address.line2},` : ''} ${address.city}, ${address.state}, ${address.country}, ${address.postal_code}.` },
            ),
          ],
        },
      )
    },
  },
  {
    title: 'ID',
    key: 'employee_id',
    width: 45,
  },
  {
    title: 'User',
    key: 'user',
    render: ({ user }) => {
      return h(
        NSpace,
        { align: 'center' },
        {
          default: () => [
            h(
              NAvatar,
              {
                round: true,
                size: 'small',
                src: user.avatar_url,
                fallbackSrc: `https://ui-avatars.com/api/?name=${user.first_name}+${user.last_name}`,
              },
            ),
            h(
              NText,
              { strong: true },
              { default: () => `${user.first_name} ${user.last_name}` },
            ),
          ],
        },
      )
    },
    sorter: (row1, row2) => row1.user.first_name.localeCompare(row2.user.first_name),
  },
  {
    title: 'Salary',
    key: 'salary',
    render: ({ salary }) => {
      return h(
        NP,
        {},
        { default: () => `RM ${salary}` },
      )
    },
    sorter: (row1, row2) => parseFloat(row1.salary) - parseFloat(row2.salary),
  },
  {
    title: 'Role',
    key: 'role',
    render: ({ role }) => {
      const type = role === 'manager' ? 'success' : role === 'admin' ? 'info' : role === 'cashier' ? 'warning' : undefined
      return h(
        NTag,
        { type },
        { default: () => `${role.charAt(0).toUpperCase()}${role.substr(1)}` },
      )
    },
    sorter: (row1, row2) => row1.role.localeCompare(row2.role),
    filterOptions: [
      {
        label: 'Manager',
        value: 'manager',
      },
      {
        label: 'Cashier',
        value: 'cashier',
      },
      {
        label: 'Runner',
        value: 'runner',
      },
      {
        label: 'Admin',
        value: 'admin',
      },
    ],
    filter: (value, row) => row.role === value,
  },
  {
    title: 'Department',
    key: 'department',
    render: ({ department }) => {
      return h(
        NP,
        {},
        { default: () => `${department.name}` },
      )
    },
    sorter: (row1, row2) => row1.department.name.localeCompare(row2.department.name),
  },
  {
    title: 'Work Period',
    key: 'work_period',
    render: ({ start_at, end_at }) => {
      return `${format(new Date(start_at), dateFormat.value)} - ${end_at ? format(new Date(end_at), dateFormat.value) : 'present'}`
    },
    sorter: (row1, row2) => compareAsc(new Date(row1.start_at), new Date(row2.start_at)),
    filterOptions: [
      {
        label: 'Still working',
        value: 'present',
      },
      {
        label: 'Resigned',
        value: 'resigned',
      },
    ],
    filter: (value, row) => value === 'resigned' ? !!row.end_at : !row.end_at,
  },
  {
    title: 'Actions',
    key: 'actions',
    render: (row) => {
      return h(
        NSpace,
        {},
        {
          default: () => [
            h(
              NButton,
              { tertiary: true, circle: true, type: 'info', onClick: () => editing.value = { employee: row, isEditing: true } },
              {
                icon: () => h(
                  NIcon,
                  {},
                  { default: () => h(Edit) },
                ),
              },
            ),
            h(
              NButton,
              { tertiary: true, circle: true, type: 'error', onClick: () => deleteEmployee(row.user.username) },
              {
                icon: () => h(
                  NIcon,
                  {},
                  { default: () => h(Delete) },
                ),
              },
            ),
          ],
        },
      )
    },
  },
]
</script>

<template>
  <n-space vertical>
    <n-space justify="space-between" align="center">
      <p>You have selected {{ checkedRowKeys.length }} row.</p>

      <n-space>
        <n-button ghost type="error" icon-placement="right" @click="bulkDeleteEmployee">
          <template #icon>
            <n-icon>
              <delete />
            </n-icon>
          </template>
          Bulk Delete
        </n-button>
        <n-button icon-placement="right" @click="() => addFormOpen = true">
          <template #icon>
            <n-icon>
              <add />
            </n-icon>
          </template>
          Add Employee
        </n-button>
      </n-space>
    </n-space>

    <n-data-table
      v-model:checked-row-keys="checkedRowKeys"
      :row-key="(data) => data.employee_id"
      :loading="data === undefined"
      :columns="columns"
      :data="sortedData"
      :pagination="pagination"
    />
  </n-space>
  <n-drawer v-model:show="editing.isEditing" :width="450">
    <n-drawer-content
      :title="editing.employee ? `${editing.employee.user.first_name} ${editing.employee.user.last_name}` : ''"
    >
      <n-form ref="editingFormRef" size="small" :model="editingFormModel">
        <n-grid :span="24" :x-gap="4">
          <n-form-item-gi
            :span="12"
            label="First Name"
            path="editingFormModel.userValue.first_name"
          >
            <n-input
              v-model:value="editingFormModel.userValue.first_name"
              placeholder="First Name"
            />
          </n-form-item-gi>
          <n-form-item-gi :span="12" label="Last Name" path="editingFormModel.userValue.last_name">
            <n-input v-model:value="editingFormModel.userValue.last_name" placeholder="Last Name" />
          </n-form-item-gi>
          <n-form-item-gi :span="12" label="Username" path="editingFormModel.userValue.username">
            <n-input
              v-model:value="editingFormModel.userValue.username"
              disabled
              placeholder="Username"
            />
          </n-form-item-gi>
          <n-form-item-gi :span="12" label="Email" path="editingFormModel.userValue.email">
            <n-input v-model:value="editingFormModel.userValue.email" placeholder="Email" />
          </n-form-item-gi>
          <n-form-item-gi
            :span="12"
            label="Phone Number"
            path="editingFormModel.userValue.phone_number"
          >
            <n-input
              v-model:value="editingFormModel.userValue.phone_number"
              placeholder="Phone Number"
            />
          </n-form-item-gi>
          <n-form-item-gi :span="12" label="Date of Birth" path="editingFormModel.userValue.dob">
            <n-date-picker v-model:value="editingFormModel.userValue.dob" type="date" />
          </n-form-item-gi>
          <n-form-item-gi :span="24" label="Gender" path="editingFormModel.userValue.gender">
            <n-select
              v-model:value="editingFormModel.userValue.gender"
              placeholder="Gender"
              :options="genderOptions"
            />
          </n-form-item-gi>
          <n-form-item-gi :span="12" label="Start At" path="editingFormModel.startAtValue">
            <n-date-picker v-model:value="editingFormModel.startAtValue" type="date" />
          </n-form-item-gi>
          <n-form-item-gi :span="12" label="End At" path="editingFormModel.endAtValue">
            <n-date-picker v-model:value="editingFormModel.endAtValue" type="date" />
          </n-form-item-gi>
          <n-form-item-gi :span="12" label="Role" path="editingFormModel.roleValue">
            <n-select
              v-model:value="editingFormModel.roleValue"
              placeholder="Role"
              :options="roleOptions"
            />
          </n-form-item-gi>
          <n-form-item-gi :span="12" label="Salary" path="editingFormModel.salaryValue">
            <n-input-number v-model:value="editingFormModel.salaryValue">
              <template #prefix>
                RM
              </template>
            </n-input-number>
          </n-form-item-gi>
        </n-grid>
      </n-form>
      <template #footer>
        <n-button
          ghost
          type="error"
          class="mr-2"
          @click="() => editing = { employee: null, isEditing: false }"
        >
          Cancel
        </n-button>
        <n-button type="success">
          Apply
        </n-button>
      </template>
    </n-drawer-content>
  </n-drawer>

  <n-drawer v-model:show="addFormOpen" :width="460">
    <n-drawer-content>
      <n-form ref="addFormRef" size="small" :model="addFormModel">
        <n-grid :span="24" :x-gap="4">
          <n-form-item-gi :span="24">
            <n-h2 class="mb-0">User</n-h2>
          </n-form-item-gi>
          <n-form-item-gi
            :span="12"
            label="First Name"
            path="addFormModel.userValue.first_name"
          >
            <n-input
              v-model:value="addFormModel.userValue.first_name"
              placeholder="First Name"
            />
          </n-form-item-gi>
          <n-form-item-gi :span="12" label="Last Name" path="addFormModel.userValue.last_name">
            <n-input v-model:value="addFormModel.userValue.last_name" placeholder="Last Name" />
          </n-form-item-gi>
          <n-form-item-gi :span="12" label="Username" path="addFormModel.userValue.username">
            <n-input
              v-model:value="addFormModel.userValue.username"
              disabled
              placeholder="Username"
            />
          </n-form-item-gi>
          <n-form-item-gi :span="12" label="Email" path="addFormModel.userValue.email">
            <n-input v-model:value="addFormModel.userValue.email" placeholder="Email" />
          </n-form-item-gi>
          <n-form-item-gi
            :span="12"
            label="Phone Number"
            path="addFormModel.userValue.phone_number"
          >
            <n-input
              v-model:value="addFormModel.userValue.phone_number"
              placeholder="Phone Number"
            />
          </n-form-item-gi>
          <n-form-item-gi :span="12" label="Date of Birth" path="addFormModel.userValue.dob">
            <n-date-picker v-model:value="addFormModel.userValue.dob" type="date" />
          </n-form-item-gi>
          <n-form-item-gi :span="24" label="Gender" path="addFormModel.userValue.gender">
            <n-select
              v-model:value="addFormModel.userValue.gender"
              placeholder="Gender"
              :options="genderOptions"
            />
          </n-form-item-gi>
          <n-form-item-gi :span="24">
            <n-h2 class="mb-0">
              Employee
            </n-h2>
          </n-form-item-gi>
          <n-form-item-gi :span="24" label="Department" path="addFormModel.departmentValue.name">
            <n-select
              v-model:value="addFormModel.departmentValue.name"
              placeholder="Department"
              :options="departmentOptions"
            />
          </n-form-item-gi>
          <n-form-item-gi :span="12" label="Start At" path="addFormModel.startAtValue">
            <n-date-picker v-model:value="addFormModel.startAtValue" type="date" />
          </n-form-item-gi>
          <n-form-item-gi :span="12" label="End At" path="addFormModel.endAtValue">
            <n-date-picker v-model:value="addFormModel.endAtValue" type="date" />
          </n-form-item-gi>
          <n-form-item-gi :span="12" label="Role" path="addFormModel.roleValue">
            <n-select
              v-model:value="addFormModel.roleValue"
              placeholder="Role"
              :options="roleOptions"
            />
          </n-form-item-gi>
          <n-form-item-gi :span="12" label="Salary" path="addFormModel.salaryValue">
            <n-input-number v-model:value="addFormModel.salaryValue" placeholder="Salary">
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
          <n-form-item-gi :span="24" label="Address Line 1" path="addFormModel.addressValue.line1">
            <n-input
              v-model:value="addFormModel.addressValue.line1"
              placeholder="Address Line 1"
            />
          </n-form-item-gi>
          <n-form-item-gi :span="24" label="Address Line 2" path="addFormModel.addressValue.line2">
            <n-input
              v-model:value="addFormModel.addressValue.line2"
              placeholder="Address Line 2"
            />
          </n-form-item-gi>
          <n-form-item-gi :span="12" label="City" path="addFormModel.addressValue.city">
            <n-input
              v-model:value="addFormModel.addressValue.city"
              placeholder="City"
            />
          </n-form-item-gi>
          <n-form-item-gi :span="12" label="State" path="addFormModel.addressValue.state">
            <n-input
              v-model:value="addFormModel.addressValue.state"
              placeholder="State"
            />
          </n-form-item-gi>
          <n-form-item-gi :span="12" label="Postal Code" path="addFormModel.addressValue.postal_code">
            <n-input
              v-model:value="addFormModel.addressValue.postal_code"
              placeholder="Postal Code"
            />
          </n-form-item-gi>
          <n-form-item-gi :span="12" label="Country" path="addFormModel.addressValue.country">
            <n-input
              v-model:value="addFormModel.addressValue.country"
              placeholder="Country"
            />
          </n-form-item-gi>
        </n-grid>
      </n-form>
      <template #footer>
        <n-button
          ghost
          type="error"
          class="mr-2"
          @click="() => addFormOpen = false"
        >
          Cancel
        </n-button>
        <n-button type="success">
          Apply
        </n-button>
      </template>
    </n-drawer-content>
  </n-drawer>
</template>
