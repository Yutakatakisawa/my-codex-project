import wixData from 'wix-data';
import wixLocation from 'wix-location';

const COLLECTION_NAME = 'ShindanResponses';
const QUESTION_IDS = Array.from({ length: 20 }, (_, index) => `q${index + 1}`);

const CATEGORY_CONFIG = [
  { key: 'discoverability', label: '見つかりやすさ', questionIds: ['q1', 'q2', 'q3', 'q4'] },
  { key: 'trust', label: '信頼性', questionIds: ['q5', 'q6', 'q7', 'q8'] },
  { key: 'funnel', label: '導線', questionIds: ['q9', 'q10', 'q11', 'q12'] },
  { key: 'followup', label: '追客', questionIds: ['q13', 'q14', 'q15', 'q16'] },
  { key: 'operations', label: '運用継続', questionIds: ['q17', 'q18', 'q19', 'q20'] }
];

// 同点時の優先順位: 導線 > 見つかりやすさ > 信頼性 > 追客 > 運用継続
const WEAKEST_PRIORITY = ['funnel', 'discoverability', 'trust', 'followup', 'operations'];

const RESULT_TYPES = [
  { id: 'D', min: 0, max: 39, name: 'Type D：緊急改善型' },
  { id: 'C', min: 40, max: 64, name: 'Type C：土台再構築型' },
  { id: 'B', min: 65, max: 84, name: 'Type B：伸びしろ加速型' },
  { id: 'A', min: 85, max: 100, name: 'Type A：自動集客準備完了型' }
];

$w.onReady(() => {
  resetError();
  setSubmitLoading(false);

  $w('#submitBtn').onClick(async () => {
    await submitDiagnostic();
  });
});

async function submitDiagnostic() {
  resetError();
  setSubmitLoading(true);

  const missingBasics = getMissingBasicFields();
  const { answers, unansweredQuestions } = collectAnswers();

  if (missingBasics.length > 0 || unansweredQuestions.length > 0) {
    const messageParts = [];

    if (missingBasics.length > 0) {
      messageParts.push('お名前・業種・地域を入力してください。');
    }

    if (unansweredQuestions.length > 0) {
      messageParts.push(`未回答の設問があります（${unansweredQuestions.length}問）。`);
    }

    showError(messageParts.join(' '));
    setSubmitLoading(false);
    return;
  }

  const totalScore = QUESTION_IDS.reduce((sum, questionId) => sum + answers[questionId], 0);
  const score100 = Math.round((totalScore / (QUESTION_IDS.length * 3)) * 100);
  const categoryScores = calculateCategoryScores(answers);
  const weakestCategory = pickWeakestCategory(categoryScores);
  const resultType = pickResultType(score100);

  const payload = {
    name: getTextValue('#nameInput'),
    industry: getTextValue('#industryDropdown'),
    area: getTextValue('#areaInput'),
    totalScore,
    score100,
    resultType: resultType.id,
    weakestCategory: weakestCategory.label,
    createdAt: new Date()
  };

  QUESTION_IDS.forEach((questionId) => {
    payload[questionId] = answers[questionId];
  });

  try {
    const inserted = await wixData.insert(COLLECTION_NAME, payload);
    wixLocation.to(`/shindan-result?rid=${inserted._id}`);
  } catch (error) {
    console.error('診断データ保存エラー:', error);
    showError('保存に失敗しました。時間をおいて再度お試しください。');
    setSubmitLoading(false);
  }
}

function getMissingBasicFields() {
  const missing = [];

  if (!getTextValue('#nameInput')) {
    missing.push('name');
  }
  if (!getTextValue('#industryDropdown')) {
    missing.push('industry');
  }
  if (!getTextValue('#areaInput')) {
    missing.push('area');
  }

  return missing;
}

function collectAnswers() {
  const answers = {};
  const unansweredQuestions = [];

  QUESTION_IDS.forEach((questionId) => {
    const rawValue = $w(`#${questionId}`).value;
    const parsedValue = Number(rawValue);

    if (rawValue === '' || rawValue === null || rawValue === undefined || Number.isNaN(parsedValue)) {
      unansweredQuestions.push(questionId);
      return;
    }

    answers[questionId] = parsedValue;
  });

  return { answers, unansweredQuestions };
}

function calculateCategoryScores(answers) {
  const scores = {};

  CATEGORY_CONFIG.forEach((category) => {
    const raw = category.questionIds.reduce((sum, questionId) => sum + answers[questionId], 0);
    const percent = Math.round((raw / (category.questionIds.length * 3)) * 100);

    scores[category.key] = {
      key: category.key,
      label: category.label,
      raw,
      percent
    };
  });

  return scores;
}

function pickWeakestCategory(categoryScores) {
  let weakest = categoryScores[WEAKEST_PRIORITY[0]];

  WEAKEST_PRIORITY.forEach((key) => {
    if (categoryScores[key].raw < weakest.raw) {
      weakest = categoryScores[key];
    }
  });

  return weakest;
}

function pickResultType(score100) {
  const matched = RESULT_TYPES.find((typeConfig) => score100 >= typeConfig.min && score100 <= typeConfig.max);
  return matched || RESULT_TYPES[0];
}

function getTextValue(selector) {
  const value = $w(selector).value;
  if (typeof value === 'string') {
    return value.trim();
  }
  return value;
}

function showError(message) {
  $w('#errorText').text = message;
  if ($w('#errorText').collapsed) {
    $w('#errorText').expand();
  }
}

function resetError() {
  $w('#errorText').text = '';
  if (!$w('#errorText').collapsed) {
    $w('#errorText').collapse();
  }
}

function setSubmitLoading(isLoading) {
  if (isLoading) {
    $w('#submitBtn').label = '診断結果を作成中...';
    $w('#submitBtn').disable();
    return;
  }

  $w('#submitBtn').label = '診断結果を見る';
  $w('#submitBtn').enable();
}
