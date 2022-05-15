<template>
  <div class="uk-grid-collapse pmi-border uk-border-rounded uk-background-default" uk-grid>
    <div class="pmi-width-extra-small pm-background-darkblue uk-visible@m">

    </div>
    <div class="uk-width-2-5 uk-margin-small uk-margin-small-left uk-margin-small-right ">
      <p class="uk-margin-remove">ID: 000000</p>
      <table class="uk-table-small uk-width-expand uk-padding-small ">

        <tbody>
        <caption style="font-size: 21px" class="uk-margin-remove pm-color-darkblue uk-text-bold uk-text-justify uk-width-expand">Bone marrow examination</caption>
          <tr>
            <td class="uk-padding-remove">Doctor: </td>
            <td class="uk-padding-remove uk-text-right">Adam Mickiewicz</td>
          </tr>
          <tr>
            <td class="uk-padding-remove">Room: </td>
            <td class="uk-padding-remove uk-text-right">001</td>
          </tr>
          <tr>
            <td class="uk-padding-remove">Date: </td>
            <td class="uk-padding-remove uk-text-right">14.05.2022</td>
          </tr>
          <tr>
            <td class="uk-padding-remove">Status: </td>
            <td class="uk-padding-remove uk-text-right">ACTIVE</td>
          </tr>
        </tbody>
      </table>
    </div>
    <div class=" uk-width-2-5 uk-margin-small uk-margin-small-left uk-margin-small-right uk-margin-auto-vertical pmi-border-left">
      <table class="uk-margin-small-left uk-table-small uk-width-expand uk-padding-small">
        <caption style="font-size: 21px" class="uk-margin-remove pm-color-darkblue uk-text-bold uk-text-justify ">Jan Kowalski</caption>
          <tr>
            <td class="uk-padding-remove">ID: </td>
            <td class="uk-padding-remove uk-text-right">89051406858</td>
          </tr>
          <tr>
            <td class="uk-padding-remove">Age: </td>
            <td class="uk-padding-remove uk-text-right">25 Years</td>
          </tr>
          <tr>
            <td class="uk-padding-remove">Contact: </td>
            <td class="uk-padding-remove uk-text-right">799 456 123</td>
          </tr>
      </table>
    </div>
    <div class="uk-width-expand@m uk-text-center uk-margin-auto-vertical uk-margin-small uk-margin-small-left uk-margin-small-right ">
      <a href="#"><button style="font-size: 16px" class="uk-button pm-button-primary uk-button-small uk-width-small uk-margin-small-bottom uk-margin-small-top">View Details</button></a>
    </div>
  </div>
</template>

<script>
export default {
  name: "ActiveTestComponent"
}
</script>

<style scoped>
.pmi-border{
  border-width: 2px;
  border-style: solid;
  border-color: #08415C;
}
.pmi-border-left{
  border-left-width: 2px;
  border-left-style: solid;
  border-left-color: #08415C;
}
.pmi-width-extra-small{
  width: 2%;
}
</style>