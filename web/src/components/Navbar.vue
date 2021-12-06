<script setup lang="ts">
import { NA, NButton } from 'naive-ui'
import { Dashboard, Help } from '@vicons/carbon'
import { isDark, toggleDark } from '~/composables'

const help = () => {
  alert('Not implemented')
}
</script>

<template>
  <nav class="text-xl px-4 py-4 w-full">
    <div flex="~" justify="between" align="items-center">
      <router-link to="/" #="{ navigate, href }" custom>
        <n-a :href="href" @click="navigate">
          <n-button quaternary>
            <template #icon>
              <dashboard />
            </template>
            Dashboard
          </n-button>
        </n-a>
      </router-link>

      <div flex="~" align="items-center">
        <n-button quaternary @click="toggleDark()">
          <carbon-moon v-if="isDark" />
          <carbon-sun v-else />
        </n-button>

        <n-button quaternary @click="help">
          <carbon-help />
        </n-button>
      </div>
    </div>
  </nav>
</template>
