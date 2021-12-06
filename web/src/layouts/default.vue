<script setup lang="ts">
import { NDivider } from 'naive-ui'
</script>

<template>
  <Navbar />
  <n-divider :style="{ margin: 0 }" />
  <main class="px-4 py-8 text-center text-gray-700 dark:text-gray-200">
    <router-view />
    <Footer />
  </main>
</template>
