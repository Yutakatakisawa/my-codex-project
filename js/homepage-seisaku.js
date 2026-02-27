(() => {
  const LINE_ADD_FRIEND_URL = "https://lin.ee/REPLACE_ME";
  const STORAGE_KEY = "shokuninWebDiagnoses";

  const CATEGORY_CONFIG = [
    { key: "discoverability", label: "見つかりやすさ", ids: ["q1", "q2", "q3", "q4"] },
    { key: "trust", label: "信頼性", ids: ["q5", "q6", "q7", "q8"] },
    { key: "funnel", label: "導線", ids: ["q9", "q10", "q11", "q12"] },
    { key: "followup", label: "追客", ids: ["q13", "q14", "q15", "q16"] },
    { key: "operations", label: "運用継続", ids: ["q17", "q18", "q19", "q20"] }
  ];

  const WEAKEST_PRIORITY = ["funnel", "discoverability", "trust", "followup", "operations"];

  const RESULT_TYPES = [
    {
      id: "D",
      min: 0,
      max: 39,
      title: "Type D：緊急改善型",
      lead: "今は「紹介が止まると売上も止まる」状態です。",
      body: "原因は技術ではなく、Web導線の不足です。まず7日で問い合わせが入る最低ラインを作りましょう。",
      actions: [
        "電話・LINE・フォームの3導線を設置",
        "施工事例を3件掲載（Before/After＋説明）",
        "自動返信を設定（24時間以内返信を明記）"
      ]
    },
    {
      id: "C",
      min: 40,
      max: 64,
      title: "Type C：土台再構築型",
      lead: "土台はでき始めています。",
      body: "今足りないのは「信頼の見える化」と「導線の最適化」です。ここを整えると、問い合わせ数は一気に伸びます。",
      actions: [
        "お客様の声を3件追加",
        "フォーム項目を5つ以下に削減",
        "記事下にLINE CTAを固定設置"
      ]
    },
    {
      id: "B",
      min: 65,
      max: 84,
      title: "Type B：伸びしろ加速型",
      lead: "あと一歩で安定問い合わせゾーンです。",
      body: "改善ポイントは明確です。優先順位どおりに実行すれば成果が出ます。今は量より導線精度を高めましょう。",
      actions: [
        "CTA配置を記事内3箇所に統一",
        "LINEステップ配信を7日分セット",
        "相談予約導線（カレンダー）を追加"
      ]
    },
    {
      id: "A",
      min: 85,
      max: 100,
      title: "Type A：自動集客準備完了型",
      lead: "集客の勝ち筋ができています。",
      body: "次は仕組み化で、月5件受注を安定化する段階です。AIと自動配信を使って、運用負荷を下げながら拡大しましょう。",
      actions: [
        "記事 -> SNS -> LINE再利用フローを自動化",
        "リードスコアでHOT客を優先対応",
        "週次レポートを自動生成"
      ]
    }
  ];

  const QUESTIONS = [
    {
      id: "q1",
      title: "自社名で検索したとき、ホームページは表示されますか？",
      options: ["1ページ目の上位に出る", "1ページ目には出る", "2ページ目以降", "出ない / わからない"]
    },
    {
      id: "q2",
      title: "「地域名＋業種」で検索したときは？",
      options: ["3位以内", "10位以内", "11位以下", "対策していない"]
    },
    {
      id: "q3",
      title: "Googleビジネスプロフィールの運用状況は？",
      options: ["週1以上で投稿・写真更新", "月1程度更新", "登録のみ", "未登録"]
    },
    {
      id: "q4",
      title: "施工事例やブログ更新頻度は？",
      options: ["週1以上", "月1〜2回", "3ヶ月に1回以下", "ほぼ更新していない"]
    },
    {
      id: "q5",
      title: "サイトに掲載している施工事例数は？",
      options: ["20件以上", "10〜19件", "1〜9件", "0件"]
    },
    {
      id: "q6",
      title: "施工事例の質（写真・説明）は？",
      options: ["Before/After＋説明あり", "写真＋簡単説明あり", "写真だけ", "ほぼない"]
    },
    {
      id: "q7",
      title: "お客様の声（口コミ）掲載は？",
      options: ["10件以上", "3〜9件", "1〜2件", "なし"]
    },
    {
      id: "q8",
      title: "代表者プロフィールの充実度は？",
      options: ["顔写真・経歴・資格・対応地域あり", "顔写真と簡単な紹介あり", "会社名と電話のみ", "ほぼ情報なし"]
    },
    {
      id: "q9",
      title: "問い合わせ手段は何を置いていますか？",
      options: ["電話・LINE・フォームの3つ", "2つある", "1つだけ", "わかりづらい / ない"]
    },
    {
      id: "q10",
      title: "スマホで電話しやすい設計ですか？",
      options: ["画面下に固定電話ボタン", "ヘッダーに電話番号あり", "ページ下だけに記載", "なし"]
    },
    {
      id: "q11",
      title: "問い合わせフォームの入力負担は？",
      options: ["5項目以下", "6〜8項目", "9項目以上", "フォームがない / 動かない"]
    },
    {
      id: "q12",
      title: "問い合わせ後の返信速度は？",
      options: ["自動返信＋24時間以内返信", "48時間以内", "3日以上かかる", "返信漏れがある"]
    },
    {
      id: "q13",
      title: "LINE公式アカウントの活用状況は？",
      options: ["運用中（定期配信あり）", "開設済みだが配信少ない", "準備中", "未開設"]
    },
    {
      id: "q14",
      title: "見積提出後のフォローは？",
      options: ["自動で3回以上フォロー", "手動で1〜2回", "気が向いたときだけ", "ほぼしない"]
    },
    {
      id: "q15",
      title: "過去顧客への再アプローチは？",
      options: ["月1で実施", "季節ごとに実施", "年1回程度", "していない"]
    },
    {
      id: "q16",
      title: "問い合わせ情報の管理方法は？",
      options: ["一元管理（CRM/シート）", "メモで管理", "頭の中で管理", "管理していない"]
    },
    {
      id: "q17",
      title: "月次で数字を確認していますか？",
      options: ["流入・問合せ・成約を毎月確認", "問合せだけ確認", "たまに確認", "見ていない"]
    },
    {
      id: "q18",
      title: "SNS発信の継続状況は？",
      options: ["週3回以上", "週1回", "月1回", "ほぼ発信していない"]
    },
    {
      id: "q19",
      title: "施工写真・動画の整理は？",
      options: ["毎週整理して保存", "月1回整理", "不定期", "ほぼ整理していない"]
    },
    {
      id: "q20",
      title: "Web運用の担当は決まっていますか？",
      options: ["担当者が明確（本人/外注）", "なんとか回している", "忙しいと止まる", "完全に止まっている"]
    }
  ];

  function createQuestionCard(question, index) {
    const container = document.createElement("article");
    container.className = "q-card";
    container.innerHTML = `<p class="q-title">Q${index + 1}. ${question.title}</p>`;

    const optionGrid = document.createElement("div");
    optionGrid.className = "q-options";

    question.options.forEach((text, optionIndex) => {
      const value = String(3 - optionIndex);
      const label = document.createElement("label");
      label.className = "opt";
      label.innerHTML = `<input type="radio" name="${question.id}" value="${value}" /><span>${text}</span>`;
      optionGrid.appendChild(label);
    });

    container.appendChild(optionGrid);
    return container;
  }

  function renderQuestions() {
    const list = document.getElementById("questionList");
    if (!list) {
      return;
    }
    QUESTIONS.forEach((q, i) => {
      list.appendChild(createQuestionCard(q, i));
    });
  }

  function getValue(id) {
    const el = document.getElementById(id);
    return el ? String(el.value || "").trim() : "";
  }

  function collectAnswers() {
    const answers = {};
    const missing = [];
    QUESTIONS.forEach((q) => {
      const checked = document.querySelector(`input[name="${q.id}"]:checked`);
      if (!checked) {
        missing.push(q.id);
        return;
      }
      answers[q.id] = Number(checked.value);
    });
    return { answers, missing };
  }

  function calcCategoryScores(answers) {
    const scores = {};
    CATEGORY_CONFIG.forEach((category) => {
      const raw = category.ids.reduce((sum, id) => sum + answers[id], 0);
      const percent = Math.round((raw / 12) * 100);
      scores[category.key] = { key: category.key, label: category.label, raw, percent };
    });
    return scores;
  }

  function pickWeakest(categoryScores) {
    let weakest = categoryScores[WEAKEST_PRIORITY[0]];
    WEAKEST_PRIORITY.forEach((key) => {
      if (categoryScores[key].raw < weakest.raw) {
        weakest = categoryScores[key];
      }
    });
    return weakest;
  }

  function pickResultType(score100) {
    return RESULT_TYPES.find((type) => score100 >= type.min && score100 <= type.max) || RESULT_TYPES[0];
  }

  function showError(message) {
    const box = document.getElementById("errorBox");
    if (!box) {
      return;
    }
    box.style.display = "block";
    box.textContent = message;
  }

  function hideError() {
    const box = document.getElementById("errorBox");
    if (!box) {
      return;
    }
    box.style.display = "none";
    box.textContent = "";
  }

  function writeResult(resultType, score100, weakest, categoryScores) {
    document.getElementById("resultType").textContent = resultType.title;
    document.getElementById("resultScore").textContent = `総合スコア ${score100}/100点`;
    document.getElementById("resultWeak").textContent = `最優先改善領域: ${weakest.label}`;
    document.getElementById("resultLead").textContent = resultType.lead;
    document.getElementById("resultBody").textContent = resultType.body;

    const actionList = document.getElementById("resultActions");
    actionList.innerHTML = "";
    resultType.actions.forEach((action) => {
      const li = document.createElement("li");
      li.textContent = action;
      actionList.appendChild(li);
    });

    CATEGORY_CONFIG.forEach((category) => {
      const percent = categoryScores[category.key].percent;
      const bar = document.getElementById(`bar-${category.key}`);
      const value = document.getElementById(`val-${category.key}`);
      if (bar) {
        bar.style.width = `${percent}%`;
      }
      if (value) {
        value.textContent = `${percent}%`;
      }
    });
  }

  function saveRecord(record) {
    try {
      const existing = JSON.parse(localStorage.getItem(STORAGE_KEY) || "[]");
      existing.push(record);
      localStorage.setItem(STORAGE_KEY, JSON.stringify(existing));
    } catch (error) {
      console.warn("Failed to save local record:", error);
    }
  }

  function toCsv(rows) {
    const headers = [
      "timestamp",
      "name",
      "industry",
      "area",
      "score100",
      "resultType",
      "weakestCategory"
    ];
    const body = rows.map((row) =>
      headers
        .map((header) => String(row[header] || "").replaceAll('"', '""'))
        .map((v) => `"${v}"`)
        .join(",")
    );
    return [headers.join(","), ...body].join("\n");
  }

  function downloadCsv() {
    const rows = JSON.parse(localStorage.getItem(STORAGE_KEY) || "[]");
    if (!rows.length) {
      alert("まだ保存データがありません。");
      return;
    }
    const csv = toCsv(rows);
    const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = `shokunin-diagnosis-${new Date().toISOString().slice(0, 10)}.csv`;
    link.click();
    URL.revokeObjectURL(url);
  }

  function setup() {
    renderQuestions();

    const lineLinks = document.querySelectorAll("[data-line-link]");
    lineLinks.forEach((el) => {
      el.setAttribute("href", LINE_ADD_FRIEND_URL);
      el.setAttribute("target", "_blank");
      el.setAttribute("rel", "noopener noreferrer");
    });

    const submitBtn = document.getElementById("submitBtn");
    submitBtn.addEventListener("click", () => {
      hideError();
      const name = getValue("nameInput");
      const industry = getValue("industrySelect");
      const area = getValue("areaInput");
      const { answers, missing } = collectAnswers();

      if (!name || !industry || !area) {
        showError("お名前・業種・地域を入力してください。");
        return;
      }
      if (missing.length > 0) {
        showError(`未回答の設問があります（${missing.length}問）。`);
        return;
      }

      const totalRaw = Object.values(answers).reduce((sum, value) => sum + value, 0);
      const score100 = Math.round((totalRaw / 60) * 100);
      const categoryScores = calcCategoryScores(answers);
      const weakest = pickWeakest(categoryScores);
      const resultType = pickResultType(score100);

      writeResult(resultType, score100, weakest, categoryScores);

      const record = {
        timestamp: new Date().toISOString(),
        name,
        industry,
        area,
        score100,
        resultType: resultType.id,
        weakestCategory: weakest.label,
        ...answers
      };
      saveRecord(record);

      const result = document.getElementById("resultSection");
      result.style.display = "block";
      result.scrollIntoView({ behavior: "smooth", block: "start" });
    });

    const startBtn = document.getElementById("startDiagnosisBtn");
    startBtn.addEventListener("click", () => {
      document.getElementById("diagnosisSection").scrollIntoView({ behavior: "smooth", block: "start" });
    });

    const csvBtn = document.getElementById("downloadCsvBtn");
    csvBtn.addEventListener("click", downloadCsv);
  }

  document.addEventListener("DOMContentLoaded", setup);
})();
