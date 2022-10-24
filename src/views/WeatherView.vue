<template>
  <weather-presenter
    :loc="route.params.loc"
    :units="route.params.units"
  ></weather-presenter>
</template>

<script>
import { reactive, toRefs } from "vue";
import WeatherPresenter from "@/components/WeatherPresenter.vue";
import { useRoute } from "vue-router";

export default {
  components: { WeatherPresenter },
  setup() {
    const route = useRoute();

    const state = reactive({
      temp: 0,
      wind: 0,
      precip: 0,
    });

    // watch(
    //   () => route.params.loc,
    //   async newId => {
    //     userData.value = await fetchUser(newId)
    //   }
    // )
    // console.log(this.$router.params.loc);
    return {
      route,
      ...toRefs(state),
    };
  },
};
</script>

<style></style>
