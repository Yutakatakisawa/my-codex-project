import wixData from 'wix-data';
import wixLocation from 'wix-location';

const COLLECTION_NAME = 'ShindanResponses';
const LINE_ADD_FRIEND_URL = 'https://lin.ee/REPLACE_ME';

const QUESTION_IDS = Array.from({ length: 20 }, (_, index) => `q${index + 1}`);

const CATEGORY_CONFIG = [
  { key: 'discoverability', label: '見つかりやすさ', questionIds: ['q1', 'q2', 'q3', 'q4'] },
  { key: 'trust', label: '信頼性', questionIds: ['q5', 'q6', 'q7', 'q8'] },
  { key: 'funnel', label: '導線', questionIds: ['q9', 'q10', 'q11', 'q12'] },
  { key: 'followup', label: '追客', questionIds: ['q13', 'q14', 'q15', 'q16'] },
  { key: 'operations', label: '運用継続', questionIds: ['q17', 'q18', 'q19', 'q20'] }
];

const WEAKEST_PRIORITY = ['funnel', 'discoverability', 'trust', 'followup', 'operations'];

const RESULT_TYPES = [
  { id: 'D', min: 0, max: 39, name: 'Type D：緊急改善型' },
  { id: 'C', min: 40, max: 64, name: 'Type C：土台再構築型' },
  { id: 'B', min: 65, max: 84, name: 'Type B：伸びしろ加速型' },
  { id: 'A', min: 85, max: 100, name: 'Type A：自動集客準備完了型' }
];

const RESULT_COPY = {
  D: {
    lead: '今は「紹介が止まると売上も止まる」状態です。',
    body: '原因は技術ではなく、Web導線の不足です。まず7日で問い合わせが入る最低ラインを作りましょう。',
    actions: [
      '電話・LINE・フォームの3導線を設置',
      '施工事例を3件掲載（Before/After＋説明）',
      '自動返信を設定（24時間以内返信を明記）'
    ]
  },
  C: {
    lead: '土台はでき始めています。',
    body: '今足りないのは「信頼の見える化」と「導線の最適化」です。ここを整えると、問い合わせ数は一気に伸びます。',
    actions: [
      'お客様の声を3件追加',
      'フォーム項目を5つ以下に削減',
      '記事下にLINE CTAを固定設置'
    ]
  },
  B: {
    lead: 'あと一歩で安定問い合わせゾーンです。',
    body: '改善ポイントは明確です。優先順位どおりに実行すれば成果が出ます。今は量より導線精度を高めましょう。',
    actions: [
      'CTA配置を記事内3箇所に統一',
      'LINEステップ配信を7日分セット',
      '相談予約導線（カレンダー）を追加'
    ]
  },
  A: {
    lead: '集客の勝ち筋ができています。',
    body: '次は仕組み化で、月5件受注を安定化する段階です。AIと自動配信を使って、運用負荷を下げながら拡大しましょう。',
    actions: [
      '記事→SNS→LINEの再利用フローを自動化',
      'リードスコアでHOT客を優先対応',
      '週次レポートを自動生成'
    ]
  }
};

$w.onReady(async () => {
  setLineButton();

  const rid = wixLocation.query.rid;
  if (!rid) {
    renderError('診断IDが見つかりません。もう一度診断を実行してください。');
    return;
  }

  try {
    const record = await wixData.get(COLLECTION_NAME, rid);
    renderResult(record);
  } catch (error) {
    console.error('診断結果取得エラー:', error);
    renderError('診断結果の取得に失敗しました。時間をおいて再度お試しください。');
  }
});

function renderResult(record) {
  const answers = normalizeAnswers(record);
  const totalScore =
    Number.isFinite(Number(record.totalScore)) ? Number(record.totalScore) : QUESTION_IDS.reduce((sum, id) => sum + answers[id], 0);
  const score100 =
    Number.isFinite(Number(record.score100)) ? Number(record.score100) : Math.round((totalScore / (QUESTION_IDS.length * 3)) * 100);
  const categoryScores = calculateCategoryScores(answers);
  const weakestCategory = record.weakestCategory || pickWeakestCategory(categoryScores).label;
  const resultType = pickResultType(score100);
  const copy = RESULT_COPY[resultType.id];

  setText('#typeTitle', resultType.name);
  setText('#scoreText', `総合スコア ${score100}/100点`);
  setText('#weakText', `最優先改善領域：${weakestCategory}`);
  setText('#resultLeadText', copy.lead);
  setText('#resultBody', copy.body);
  setText('#action1', `1. ${copy.actions[0]}`);
  setText('#action2', `2. ${copy.actions[1]}`);
  setText('#action3', `3. ${copy.actions[2]}`);

  setText(
    '#lineLeadText',
    '診断結果を見るだけでは売上は変わりません。あなた専用の7日改善プランをLINEで無料配布します。'
  );

  // 任意でスコア表示要素を置いた場合に自動反映
  setTextIfExists('#scoreDiscoverability', `${categoryScores.discoverability.percent}%`);
  setTextIfExists('#scoreTrust', `${categoryScores.trust.percent}%`);
  setTextIfExists('#scoreFunnel', `${categoryScores.funnel.percent}%`);
  setTextIfExists('#scoreFollowup', `${categoryScores.followup.percent}%`);
  setTextIfExists('#scoreOperations', `${categoryScores.operations.percent}%`);
}

function renderError(message) {
  setText('#typeTitle', '診断結果を表示できません');
  setText('#scoreText', '');
  setText('#weakText', '');
  setText('#resultLeadText', message);
  setText('#resultBody', 'お手数ですが、診断ページから再度お試しください。');
  setText('#action1', '');
  setText('#action2', '');
  setText('#action3', '');
}

function setLineButton() {
  const button = getElement('#lineBtn');
  if (!button) {
    return;
  }

  button.label = 'LINEで7日改善プランを受け取る';
  button.link = LINE_ADD_FRIEND_URL;
}

function normalizeAnswers(record) {
  const answers = {};

  QUESTION_IDS.forEach((questionId) => {
    const value = Number(record[questionId]);
    answers[questionId] = Number.isFinite(value) ? value : 0;
  });

  return answers;
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

function setText(selector, value) {
  const element = getElement(selector);
  if (!element) {
    return;
  }
  element.text = value;
}

function setTextIfExists(selector, value) {
  const element = getElement(selector);
  if (!element) {
    return;
  }
  element.text = value;
}

function getElement(selector) {
  try {
    return $w(selector);
  } catch (error) {
    return null;
  }
}
