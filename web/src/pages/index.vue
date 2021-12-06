<script setup lang="ts">
import { NAvatar, NDataTable, NDescriptions, NDescriptionsItem, NP, NText, NSpace, NTag, NButton, NIcon } from 'naive-ui'
import type { DataTableColumn } from 'naive-ui'
import { format, compareAsc } from 'date-fns'
import { Add, Edit, Delete } from '@vicons/carbon'
import type { EmployeeView } from '~/types'

const dataOpts = ref<{ cursor?: number; limit: number }>({ limit: 1000 })
const { data } = useFetch<EmployeeView[]>(`${import.meta.env.VITE_SERVER_URL}/employees?limit=${dataOpts.value.limit}`).get().json<EmployeeView[]>()
const checkedRowKeys = ref([])
const dateFormat = ref('dd/MM/yyyy')

const sortedData = computed(() => data.value ? data.value.sort((a, b) => a.employee_id - b.employee_id) : undefined)

const pagination = {
  pageSize: 10,
}

const addEmployee = () => {
  alert('Not implemented')
}

const editEmployee = () => {
  alert('Not implemented')
}

const deleteEmployee = () => {
  alert('Not implemented')
}

const bulkDeleteEmployee = () => {
  alert('Not implemented')
}

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
    render: () => {
      return h(
        NSpace,
        {},
        {
          default: () => [
            h(
              NButton,
              { tertiary: true, circle: true, type: 'info', onClick: editEmployee },
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
              { tertiary: true, circle: true, type: 'error', onClick: deleteEmployee },
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
</template>
