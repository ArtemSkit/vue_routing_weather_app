<script setup>
import { defineProps } from "vue";
const props = defineProps(["loc", "units"]);
</script>

<template>
  <H1>Weather in {{ props.loc }}</H1>
  <p>Temp: {{}}</p>
  <p>Wind speed: {{}}</p>
  <p>Precipitation % chanse: {{}}</p>
</template>
