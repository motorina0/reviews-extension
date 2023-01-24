async function surveyItems(path) {
  const template = await loadTemplateAsync(path)
  Vue.component('survey-items', {
    name: 'survey-items',
    template,

    props: ['survey-id', 'adminkey', 'inkey'],
    data: function () {
      return {
        items: [],

        formDialogItem: {
          show: false,
          data: {
            name: '',
            description: ''
          }
        }
      }
    },

    methods: {
      satBtc(val, showUnit = true) {
        return satOrBtc(val, showUnit, this.satsDenominated)
      },

      showNewItemDialog: function () {
        this.formDialogItem.data = {
          name: '',
          description: ''
        }
        this.formDialogItem.show = true
      },

      submitSurveyItem: function () {
        this.formDialogItem.show = false
        this.addSurveyItem(this.formDialogItem.data)
      },

      getSurveyItems: async function () {
        try {
          const {data} = await LNbits.api.request(
            'GET',
            '/reviews/api/v1/survey/item/' + this.surveyId,
            this.inkey
          )
          this.items = data
        } catch (error) {
          LNbits.utils.notifyApiError(error)
        }
      },

      addSurveyItem: async function (data) {
        try {
          const resp = await LNbits.api.request(
            'POST',
            '/reviews/api/v1/survey/item',
            this.adminkey,
            {...data, survey_id: this.surveyId}
          )

          this.items.unshift(resp.data)
          this.formDialogSurvey.show = false
        } catch (error) {
          LNbits.utils.notifyApiError(error)
        }
      },

      deleteSurveyItem: async function (surveyItemId) {
        LNbits.utils
          .confirmDialog('Are you sure you want to delete this item?')
          .onOk(async () => {
            try {
              await LNbits.api.request(
                'DELETE',
                '/reviews/api/v1/survey/item/' + surveyItemId,
                this.adminkey
              )

              this.items = _.reject(this.items, function (obj) {
                return obj.id === surveyItemId
              })
            } catch (error) {
              LNbits.utils.notifyApiError(error)
            }
          })
      }
    },

    created: async function () {
      await this.getSurveyItems()
    }
  })
}
