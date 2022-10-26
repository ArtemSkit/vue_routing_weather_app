<script setup>
import { defineProps, onBeforeUpdate, ref } from "vue";
const props = defineProps(["loc", "units"]);
let lat = 0;
// let lon = 0;
let temp = ref(0);
onBeforeUpdate(async () => {
  let { street, city, zip } = props.loc.split("|");
  try {
    lat = await fetch(
      `https://geocoding.geo.census.gov/geocoder/locations/address?street=${street}&city=${city}&zip=${zip}&benchmark=Public_AR_Census2020&format=json`
    );
    console.log(lat);
  } catch (err) {
    console.error(err);
  }
});
</script>

<template>
  <h1>Weather at {{ props.loc.replaceAll("|", ", ") }}</h1>
  <p>Temp: {{ temp }}</p>
  <p>Wind speed: {{}}</p>
  <p>Precipitation % chanse: {{}}</p>
</template>
