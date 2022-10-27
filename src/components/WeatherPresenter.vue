<script setup>
import { defineProps, onBeforeMount, ref } from "vue";
const props = defineProps(["loc", "units"]);
let weatherData = ref({});
onBeforeMount(async () => {
  let [street, city, state, zip_code] = props.loc.split("|");

  try {
    // lat = await fetch(
    //   `https://geocoding.geo.census.gov/geocoder/locations/address?street=${street}&city=${city}&zip=${zip}&benchmark=Public_AR_Census2020&format=json`
    // );

    let req = await fetch(`http://localhost:8000/weather/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        street: street,
        city: city,
        state: state,
        zip_code: parseInt(zip_code),
        style: "f",
      }),
    });

    weatherData.value = await req.json();

    console.log(weatherData);
  } catch (err) {
    console.error(err);
  }
});
</script>

<template>
  <h1>Weather at {{ props.loc.replaceAll("|", ", ") }}</h1>
  <p>Temp: {{ weatherData.temperature }}</p>
  <p>Wind speed: {{ weatherData.windSpeed }}</p>
  <p>Relative humidity: {{ weatherData.relativeHumidity }}%</p>
</template>
