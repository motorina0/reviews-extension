const survey = async () => {
  Vue.component(VueQrcode.name, VueQrcode)

  await surveyItems('/reviews/static/components/survey-items/survey-items.html')

  new Vue({
    el: '#vue',
    mixins: [windowMixin],
    data: function () {
      return {}
    },
    methods: {},
    created: async function () {}
  })
}

survey()
