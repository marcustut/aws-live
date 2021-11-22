<script setup lang="ts">
// https://github.com/vueuse/head
// you can use this to manipulate the document head in any components,
// they will be rendered correctly in the html results with vite-ssg
useHead({
  title: 'Employee Management System',
  meta: [
    {
      name: 'description',
      content: 'A Dashboard for easily managing employees',
    },
  ],
})
</script>

<template>
  <provider>
    <viewer />
  </provider>
</template>
