const mapSurvey = (obj, oldObj = {}) => {
  const survey = {...oldObj, ...obj}

  survey.expanded = oldObj.expanded || false

  return survey
}
