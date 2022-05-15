<template>
  <div class="uk-grid-collapse" uk-grid>
    <div class="uk-width-1-5@m uk-margin-medium-top uk-padding-small">
      <form class="">
        <fieldset class="uk-fieldset">
          <div class="uk-margin">
            <legend class="uk-legend uk-text-bold uk-text-justify">Test info:</legend>
            <input class="uk-input pmi-form" type="text" placeholder="ID">
            <input class="uk-input pmi-form" type="text" placeholder="Type">
            <input class="uk-input pmi-form" type="text" placeholder="Room">
            <input class="uk-input pmi-form" type="text" placeholder="Date">
            <input class="uk-input pmi-form" type="text" placeholder="Status">
          </div>
          <div class="uk-margin">
            <legend class="uk-legend uk-text-bold uk-text-justify">Patient info:</legend>
            <input class="uk-input pmi-form" type="text" placeholder="Name">
            <input class="uk-input pmi-form" type="text" placeholder="Surname">
            <input class="uk-input pmi-form" type="text" placeholder="Personal ID">
          </div>
          <div class="uk-margin">
            <legend class="uk-legend uk-text-bold uk-text-justify">Doctor info:</legend>
            <input class="uk-input pmi-form" type="text" placeholder="Name">
            <input class="uk-input pmi-form" type="text" placeholder="Surname">
            <input class="uk-input pmi-form" type="text" placeholder="Personal ID">
          </div>
        </fieldset>
        <input class="uk-align-center pm-button-primary uk-button" type="submit" value="Search">
      </form>
    </div>

       <div class="uk-width-expand@m uk-container uk-margin-medium-top uk-padding-small pm-background-white uk-border-rounded">
      <div>
        <ul class="uk-list uk-list-large">
              <li><ActiveTest/></li>
              <li><ActiveTest/></li>
              <li><ActiveTest/></li>
          </ul>
      </div>
    </div>
  </div>
</template>

<style>
.pmi-form{
  background-color: #EEE5E9;
  border-color: #6B818C;
  border-style: solid;
  border-width: 1px;
  margin-bottom: 1%;
}
</style>


<script>
// @ is an alias to /src
import ActiveTest from "@/components/TestPanelComponent";
import '/../static/css/uikit.min.css'
import '/../static/css/pawmed.css'


export default {
  name: 'HomeView',
  components:{
    ActiveTest
  }
}
</script>

