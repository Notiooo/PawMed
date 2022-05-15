<template>
  <div class="uk-container uk-margin-medium-top pm-background-white uk-border-rounded">
    <div>
      <p style="font-size: 21px" class="uk-text-bold pm-color-darkblue uk-margin-medium-top">Active Tests</p>
    </div>
    <div>
      <ul class="uk-list uk-list-large">
            <li><ActiveTest/></li>
            <li><ActiveTest/></li>
            <li><ActiveTest/></li>
        </ul>
    </div>
  </div>

  <div class="uk-container uk-margin-medium-top pm-background-white uk-border-rounded">
    <div>
      <p style="font-size: 21px" class="uk-text-bold pm-color-darkblue uk-margin-medium-top">Recent Closed Tests</p>
    </div>
    <div>
      <ul class="uk-list uk-list-large">
            <li><ActiveTest/></li>
            <li><ActiveTest/></li>
            <li><ActiveTest/></li>
        </ul>
    </div>
  </div>
</template>




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

