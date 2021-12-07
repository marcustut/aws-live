<script setup lang="ts">
import { NConfigProvider, NNotificationProvider, NLoadingBarProvider, darkTheme } from 'naive-ui'
import { isDark } from '~/composables'
</script>

<template>
  <n-config-provider :theme="isDark ? darkTheme : undefined">
    <n-loading-bar-provider>
      <n-notification-provider>
        <slot></slot>
      </n-notification-provider>
    </n-loading-bar-provider>
  </n-config-provider>
</template>
