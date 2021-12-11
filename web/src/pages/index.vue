<script setup lang="ts">
// @ts-ignore
import {
  NAvatar,
  NUpload,
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
import { useEmployeeFormModel } from '~/composables'
import EmployeeDrawer from '~/components/EmployeeDrawer.vue'
import { useDrawerStore } from '~/stores/drawer'
import { useFormStore } from '~/stores/form'

const loadingBar = useLoadingBar()
const notification = useNotification()

const dataOpts = ref<{ cursor?: number; limit: number }>({ limit: 1000 })
const checkedRowKeys = ref<number[]>([])
const dateFormat = ref<string>('dd/MM/yyyy')
const editing = ref<{ employee: EmployeeView | null }>({ employee: null })

const drawer = useDrawerStore()
const form = useFormStore()

loadingBar.start()
const { data, onFetchError, onFetchResponse, execute } = useFetch<EmployeeView[]>(`${import.meta.env.VITE_SERVER_URL}/employees?limit=${dataOpts.value.limit}`).get().json<EmployeeView[]>()

onFetchError(() => {
  loadingBar.error()
  notification.error({ title: 'An error occurred', meta: 'Unable to fetch employees from server' })
})
onFetchResponse(() => loadingBar.finish())

const sortedData = computed(() => data.value ? data.value.sort((a, b) => a.employee_id - b.employee_id) : [])
const checkedData = computed(() => sortedData.value.length > 0 ? sortedData.value.filter(d => checkedRowKeys.value.includes(d.employee_id)) : [])
const departmentOptions = computed(() => [...new Set(sortedData.value.map(d => d.department.name))].map(n => ({ label: n, value: n })))

const pagination = { pageSize: 10 }

const handleAddEmployeeButton = () => {
  drawer.setDrawerOpen('create', true)
  form.resetFormModel('employee')
}

const handleEditEmployeeButton = (employee: EmployeeView) => {
  const { user, address, department } = employee
  drawer.setDrawerOpen('edit', true)
  form.setFormModel('employee', {
    user: {
      ...user,
      dob: new Date(user.dob).getTime(),
      avatar_url: user.avatar_url ?? '',
      avatar_image: '',
    },
    address,
    department,
    salary: parseFloat(employee.salary),
    role: employee.role,
    startAt: new Date(employee.start_at).getTime(),
    endAt: employee.end_at ? new Date(employee.end_at).getTime() : null,
  })
}

const deleteEmployee = async(username: string) => {
  loadingBar.start()
  const { onFetchError, onFetchResponse, execute } = useFetch<EmployeeView>(`${import.meta.env.VITE_SERVER_URL}/employee/${username}`, { immediate: false }).delete().json<EmployeeView>()
  onFetchError(() => {
    loadingBar.error()
    notification.error({ title: 'An error occurred', meta: `Unable to delete employee - ${username}` })
  })
  onFetchResponse(() => {
    loadingBar.finish()
    notification.success({ title: 'Successfully deleted', meta: `Employee - ${username} had been deleted` })
  })
  await execute()
}

const bulkDeleteEmployee = () => {
  if (checkedData.value.length !== 0)
    checkedData.value.forEach(async d => await deleteEmployee(d.user.username))
  else
    notification.error({ title: 'No rows are selected', meta: 'Select at least one row to bulk delete' })
}

const genderOptions = ['Male', 'Female'].map(g => ({ label: g, value: g.toLowerCase() }))
const roleOptions = ['Admin', 'Manager', 'Runner', 'Cashier'].map(g => ({ label: g, value: g.toLowerCase() }))

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
              // @ts-ignore
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
              { tertiary: true, circle: true, type: 'info', onClick: () => handleEditEmployeeButton(row) },
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
        <n-button disabled ghost type="error" icon-placement="right" @click="bulkDeleteEmployee">
          <template #icon>
            <n-icon>
              <delete />
            </n-icon>
          </template>
          Bulk Delete
        </n-button>
        <n-button icon-placement="right" @click="handleAddEmployeeButton">
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

  <employee-drawer
    type="create"
    :refetch="() => execute()"
    :department-options="departmentOptions"
    :gender-options="genderOptions"
    :role-options="roleOptions"
  />
  <employee-drawer
    type="edit"
    :refetch="() => execute()"
    :department-options="departmentOptions"
    :gender-options="genderOptions"
    :role-options="roleOptions"
  />
</template>
