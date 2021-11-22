<script setup lang="ts">
import { NP, NA } from 'naive-ui'
</script>

<template>
  <nav class="text-xl px-4 py-4 w-full">
    <div flex="~" justify="between" align="items-center">
      <router-link to="/" #="{navigate, href}" custom>
        <n-a :href="href" @click="navigate">
          <div flex="~" align="items-center" text="sm true-gray-300 hover:green-400" font="medium" transition="~ duration-200 ease-in-out">
            <carbon-campsite w="6" h="6" mr="1" />
            Dashboard
          </div>
        </n-a>
      </router-link>

      <div flex="~" align="items-center">
        <n-p m="0">
          hi
        </n-p>
      </div>
    </div>
  </nav>
</template>
