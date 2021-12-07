<script setup lang="ts">
import {
  NAvatar,
  NDataTable,
  NDrawer,
  NDrawerContent,
  NDescriptions,
  NDescriptionsItem,
  NP,
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
  useNotification
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
const editing = ref<{ employee: EmployeeView | null, isEditing: boolean }>({ employee: null, isEditing: false })
const editingFormRef = ref(null)

loadingBar.start()
const { data, onFetchError, onFetchResponse } = useFetch<EmployeeView[]>(`${import.meta.env.VITE_SERVER_URL}/employees?limit=${dataOpts.value.limit}`).get().json<EmployeeView[]>()

onFetchError(() => {
  loadingBar.error()
  notification.error({ title: `An error occured`, meta: `Unable to fetch employees from server` })
})
onFetchResponse(() => loadingBar.finish())

const sortedData = computed(() => data.value ? data.value.sort((a, b) => a.employee_id - b.employee_id) : [])
const checkedData = computed(() => sortedData.value.length > 0 ? sortedData.value.filter((d) => checkedRowKeys.value.includes(d.employee_id)) : [])

const pagination = {
  pageSize: 10,
}

const addEmployee = () => {
  alert('Not implemented')
}

const editEmployee = (employee: EmployeeView) => {
  alert('Not implemented')
}

const deleteEmployee = (username: string) => {
  loadingBar.start()
  const { onFetchError, onFetchResponse } = useFetch<EmployeeView>(`${import.meta.env.VITE_SERVER_URL}/employee/${username}`).delete().json<EmployeeView>()
  onFetchError(() => {
    loadingBar.error()
    notification.error({ title: `An error occured`, meta: `Unable to delete employee - ${username}` })
  })
  onFetchResponse(() => {
    loadingBar.finish()
    notification.success({ title: `Successfully deleted`, meta: `Employee - ${username} had been deleted` })
  })
}

const bulkDeleteEmployee = () => {
  if (checkedData.value.length !== 0)
    checkedData.value.forEach((d) => deleteEmployee(d.user.username))
  else
    notification.error({ title: 'No rows are selected', meta: 'Select at least one row to bulk delete' })
}

const genderOptions = ['Male', 'Female'].map((g) => ({ label: g, value: g.toLowerCase() }))
const roleOptions = ['Admin', 'Manager', 'Runner', 'Cashier'].map((g) => ({ label: g, value: g.toLowerCase() }))

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
        <n-button icon-placement="right" @click="addEmployee">
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
              placeholder="First Name"
              v-model:value="editingFormModel.userValue.first_name"
            />
          </n-form-item-gi>
          <n-form-item-gi :span="12" label="Last Name" path="editingFormModel.userValue.last_name">
            <n-input placeholder="Last Name" v-model:value="editingFormModel.userValue.last_name" />
          </n-form-item-gi>
          <n-form-item-gi :span="12" label="Username" path="editingFormModel.userValue.username">
            <n-input
              disabled
              placeholder="Username"
              v-model:value="editingFormModel.userValue.username"
            />
          </n-form-item-gi>
          <n-form-item-gi :span="12" label="Email" path="editingFormModel.userValue.email">
            <n-input placeholder="Email" v-model:value="editingFormModel.userValue.email" />
          </n-form-item-gi>
          <n-form-item-gi
            :span="12"
            label="Phone Number"
            path="editingFormModel.userValue.phone_number"
          >
            <n-input
              placeholder="Phone Number"
              v-model:value="editingFormModel.userValue.phone_number"
            />
          </n-form-item-gi>
          <n-form-item-gi :span="12" label="Date of Birth" path="editingFormModel.userValue.dob">
            <n-date-picker type="date" v-model:value="editingFormModel.userValue.dob" />
          </n-form-item-gi>
          <n-form-item-gi :span="24" label="Gender" path="editingFormModel.userValue.gender">
            <n-select
              placeholder="Gender"
              :options="genderOptions"
              v-model:value="editingFormModel.userValue.gender"
            />
          </n-form-item-gi>
          <n-form-item-gi :span="12" label="Start At" path="editingFormModel.startAtValue">
            <n-date-picker type="date" v-model:value="editingFormModel.startAtValue" />
          </n-form-item-gi>
          <n-form-item-gi :span="12" label="End At" path="editingFormModel.endAtValue">
            <n-date-picker type="date" v-model:value="editingFormModel.endAtValue" />
          </n-form-item-gi>
          <n-form-item-gi :span="12" label="Role" path="editingFormModel.roleValue">
            <n-select
              placeholder="Role"
              :options="roleOptions"
              v-model:value="editingFormModel.roleValue"
            />
          </n-form-item-gi>
          <n-form-item-gi :span="12" label="Salary" path="editingFormModel.salaryValue">
            <n-input-number v-model:value="editingFormModel.salaryValue">
              <template #prefix>RM</template>
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
        >Cancel</n-button>
        <n-button type="success">Apply</n-button>
      </template>
    </n-drawer-content>
  </n-drawer>
</template>
