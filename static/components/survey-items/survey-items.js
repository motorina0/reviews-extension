async function surveyItems(path) {
  const template = await loadTemplateAsync(path)
  Vue.component('survey-items', {
    name: 'survey-items',
    template,

    props: [
      'addresses',
      'accounts',
      'mempool-endpoint',
      'inkey',
      'sats-denominated'
    ],
    data: function () {
      return {
        show: false,
        history: [],
        selectedWallet: null,
        note: '',
        filterOptions: [
          'Show Change Addresses',
          'Show Gap Addresses',
          'Only With Amount'
        ],
        filterValues: [],

        addressesTable: {
          columns: [
            {
              name: 'expand',
              align: 'left',
              label: ''
            },
            {
              name: 'address',
              align: 'left',
              label: 'Address',
              field: 'address',
              sortable: true
            },
            {
              name: 'amount',
              align: 'left',
              label: 'Amount',
              field: 'amount',
              sortable: true
            },
            {
              name: 'note',
              align: 'left',
              label: 'Note',
              field: 'note',
              sortable: true
            },
            {
              name: 'wallet',
              align: 'left',
              label: 'Account',
              field: 'wallet',
              sortable: true
            }
          ],
          pagination: {
            rowsPerPage: 0,
            sortBy: 'amount',
            descending: true
          },
          filter: ''
        }
      }
    },

    methods: {
      satBtc(val, showUnit = true) {
        return satOrBtc(val, showUnit, this.satsDenominated)
      }
    },

    created: async function () {}
  })
}
