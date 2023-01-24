const reviews = async () => {
  Vue.component(VueQrcode.name, VueQrcode)

  await surveyItems('static/components/survey-items/survey-items.html')

  new Vue({
    el: '#vue',
    mixins: [windowMixin],
    data: function () {
      return {
        filter: '',
        surveyLinks: [],
        formDialogSurvey: {
          show: false,
          showAdvanced: false,
          data: {
            name: '',
            description: '',
            type: '',
            amount: '',
            wallet: ''
          }
        },
        surveyTypes: [
          {
            id: 'rating',
            label: 'Rating (rate one item from a list)'
          },
          {
            id: 'poll',
            label: 'Poll (choose one item from a list)'
          },
          {
            id: 'likes',
            label: 'Likes (like or dislike an item)'
          }
        ],

        surveysTable: {
          columns: [
            {
              name: '',
              align: 'left',
              label: '',
              field: ''
            },
            {
              name: 'name',
              align: 'left',
              label: 'Name',
              field: 'name'
            },
            {
              name: 'description',
              align: 'left',
              label: 'Description',
              field: 'description'
            },
            {
              name: 'type',
              align: 'left',
              label: 'Type',
              field: 'type'
            },
            {
              name: 'amount',
              align: 'left',
              label: 'Amount',
              field: 'amount'
            }
          ],
          pagination: {
            rowsPerPage: 10
          }
        }
      }
    },
    methods: {
      getDefaultSurveyData: function () {
        return {
          name: '',
          description: '',
          type: this.surveyTypes[0],
          amount: '100',
          wallet: ''
        }
      },
      getSurveyTypeLabel: function (surveyType) {
        const type = this.surveyTypes.find(s => (s.id = surveyType))
        return type ? type.label : '?'
      },
      openCreateSurveyDialog: function () {
        this.formDialogSurvey.data = this.getDefaultSurveyData()
        this.formDialogSurvey.show = true
      },
      getSurveys: async function () {
        try {
          const {data} = await LNbits.api.request(
            'GET',
            '/reviews/api/v1/survey',
            this.g.user.wallets[0].inkey
          )
          this.surveyLinks = data.map(c =>
            mapSurvey(
              c,
              this.surveyLinks.find(old => old.id === c.id)
            )
          )
          console.log('### surveyLinks', this.surveyLinks)
        } catch (error) {
          LNbits.utils.notifyApiError(error)
        }
      },

      createSurvey: async function (data) {
        console.log('### data', data)
        try {
          data.type = data.type.id
          const resp = await LNbits.api.request(
            'POST',
            '/reviews/api/v1/survey',
            this.g.user.wallets[0].adminkey,
            data
          )

          this.surveyLinks.unshift(mapSurvey(resp.data))
          this.formDialogSurvey.show = false
        } catch (error) {
          LNbits.utils.notifyApiError(error)
        }
      },

      deleteSurvey: function (surveyId) {
        const link = _.findWhere(this.surveyLinks, {id: surveyId})
        LNbits.utils
          .confirmDialog('Are you sure you want to delete this survet?')
          .onOk(async () => {
            try {
              const response = await LNbits.api.request(
                'DELETE',
                '/reviews/api/v1/survey/' + surveyId,
                this.g.user.wallets[0].adminkey
              )

              this.surveyLinks = _.reject(this.surveyLinks, function (obj) {
                return obj.id === surveyId
              })
            } catch (error) {
              LNbits.utils.notifyApiError(error)
            }
          })
      },

      sendFormDataSurvey: async function () {
        console.log('### sendFormDataSurvey')
        this.createSurvey(this.formDialogSurvey.data)
      },

      exportsurveyCSV: function () {
        LNbits.utils.exportCSV(
          this.surveysTable.columns,
          this.surveyLinks,
          'surveys'
        )
      }
    },
    created: async function () {
      await this.getSurveys()
    }
  })
}

reviews()
