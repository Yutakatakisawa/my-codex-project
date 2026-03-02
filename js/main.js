const FRAMEWORKS = [
  { id: "react", label: "React" },
  { id: "vue", label: "Vue" },
  { id: "svelte", label: "Svelte" },
  { id: "angular", label: "Angular" },
  { id: "solid", label: "Solid" },
];

const FRAMEWORK_ORDER = FRAMEWORKS.map((framework) => framework.id);
const FAVORITES_STORAGE_KEY = "component-gallery.favorites.v1";
const DEFAULT_COMPARE_FRAMEWORKS = ["react", "vue", "svelte"];

const COMPONENTS = [
  {
    id: "button",
    name: "Button",
    category: "Actions",
    description: "基本操作のトリガーになる主要コンポーネント。",
    preview: "button",
    tags: ["cta", "action", "primary"],
    frameworks: {
      react: {
        status: "stable",
        snippet: '<Button variant="contained">Save</Button>',
        docs: "https://mui.com/material-ui/react-button/",
        source: "https://github.com/mui/material-ui",
        note: "MUI/Chakraともに安定して利用可能",
      },
      vue: {
        status: "stable",
        snippet: '<Button label="Save" severity="primary" />',
        docs: "https://primevue.org/button/",
        source: "https://github.com/primefaces/primevue",
        note: "PrimeVueで標準提供",
      },
      svelte: {
        status: "beta",
        snippet: '<Button tone="primary">Save</Button>',
        docs: "https://www.skeleton.dev/docs/components/button",
        source: "https://github.com/skeletonlabs/skeleton",
        note: "SvelteKit向けの導入実績が増加中",
      },
      angular: {
        status: "stable",
        snippet: '<button mat-raised-button color="primary">Save</button>',
        docs: "https://material.angular.io/components/button/overview",
        source: "https://github.com/angular/components",
        note: "Angular Materialで成熟",
      },
      solid: {
        status: "planned",
        snippet: "// Planned",
        docs: "",
        source: "",
        note: "社内実装テンプレート化を予定",
      },
    },
  },
  {
    id: "icon-button",
    name: "Icon Button",
    category: "Actions",
    description: "アイコンのみで意味を伝えるコンパクトなボタン。",
    preview: "icon-button",
    tags: ["icon", "toolbar", "compact"],
    frameworks: {
      react: {
        status: "stable",
        snippet: '<IconButton aria-label="Delete"><DeleteIcon /></IconButton>',
        docs: "https://mui.com/material-ui/react-button/#icon-button",
        source: "https://github.com/mui/material-ui",
        note: "アクセシビリティ属性の付与が必須",
      },
      vue: {
        status: "beta",
        snippet: '<Button icon="pi pi-trash" rounded text aria-label="Delete" />',
        docs: "https://primevue.org/button/#icon",
        source: "https://github.com/primefaces/primevue",
        note: "デザインシステムによって形状差分が大きい",
      },
      svelte: {
        status: "beta",
        snippet: '<IconButton name="trash" ariaLabel="Delete" />',
        docs: "https://www.skeleton.dev/",
        source: "https://github.com/skeletonlabs/skeleton",
        note: "アニメーション前提の実装が多い",
      },
      angular: {
        status: "stable",
        snippet: '<button mat-icon-button aria-label="Delete"><mat-icon>delete</mat-icon></button>',
        docs: "https://material.angular.io/components/button/overview#icon-buttons",
        source: "https://github.com/angular/components",
        note: "MatIconと合わせて利用",
      },
      solid: {
        status: "planned",
        snippet: "// Planned",
        docs: "",
        source: "",
        note: "仕様策定中",
      },
    },
  },
  {
    id: "text-input",
    name: "Text Input",
    category: "Forms",
    description: "テキスト入力フォーム。バリデーションとの組み合わせが基本。",
    preview: "input",
    tags: ["form", "validation", "field"],
    frameworks: {
      react: {
        status: "stable",
        snippet: '<TextField label="Email" type="email" fullWidth />',
        docs: "https://mui.com/material-ui/react-text-field/",
        source: "https://github.com/mui/material-ui",
        note: "React Hook Formと組み合わせやすい",
      },
      vue: {
        status: "stable",
        snippet: '<InputText v-model="email" placeholder="Email" />',
        docs: "https://primevue.org/inputtext/",
        source: "https://github.com/primefaces/primevue",
        note: "v-modelでシンプルに双方向バインド",
      },
      svelte: {
        status: "stable",
        snippet: '<input class="input" bind:value={email} placeholder="Email" />',
        docs: "https://svelte.dev/docs/svelte/bind",
        source: "https://github.com/sveltejs/svelte",
        note: "bind:valueによる最小構文",
      },
      angular: {
        status: "stable",
        snippet: '<input matInput [formControl]="emailControl" placeholder="Email" />',
        docs: "https://material.angular.io/components/input/overview",
        source: "https://github.com/angular/components",
        note: "Reactive Formsとの併用が一般的",
      },
      solid: {
        status: "beta",
        snippet: '<TextField value={email()} onInput={(e) => setEmail(e.currentTarget.value)} />',
        docs: "https://www.solidjs.com/docs/latest/api#signals",
        source: "https://github.com/solidjs/solid",
        note: "Signalベースで記述",
      },
    },
  },
  {
    id: "select",
    name: "Select",
    category: "Forms",
    description: "選択肢から1つ以上を選ぶためのフォーム要素。",
    preview: "select",
    tags: ["form", "dropdown", "option"],
    frameworks: {
      react: {
        status: "stable",
        snippet: '<Select value={value} onChange={handleChange}>{options}</Select>',
        docs: "https://mui.com/material-ui/react-select/",
        source: "https://github.com/mui/material-ui",
        note: "非同期候補の扱いはAutocompleteが便利",
      },
      vue: {
        status: "stable",
        snippet: '<Select v-model="value" :options="options" optionLabel="name" />',
        docs: "https://primevue.org/select/",
        source: "https://github.com/primefaces/primevue",
        note: "Optionテンプレート拡張が柔軟",
      },
      svelte: {
        status: "beta",
        snippet: '<Select bind:value={value} items={options} />',
        docs: "https://www.skeleton.dev/docs/components/select",
        source: "https://github.com/skeletonlabs/skeleton",
        note: "カスタムUI選択肢の作り込みが必要",
      },
      angular: {
        status: "stable",
        snippet: '<mat-select [formControl]="selected"><mat-option>Option</mat-option></mat-select>',
        docs: "https://material.angular.io/components/select/overview",
        source: "https://github.com/angular/components",
        note: "テンプレート/Reactive両方に対応",
      },
      solid: {
        status: "planned",
        snippet: "// Planned",
        docs: "",
        source: "",
        note: "候補UIの仕様策定待ち",
      },
    },
  },
  {
    id: "modal",
    name: "Modal",
    category: "Feedback",
    description: "重要な確認や入力を行うためのオーバーレイダイアログ。",
    preview: "modal",
    tags: ["dialog", "overlay", "confirm"],
    frameworks: {
      react: {
        status: "stable",
        snippet: "<Dialog open={open} onClose={handleClose}>...</Dialog>",
        docs: "https://mui.com/material-ui/react-dialog/",
        source: "https://github.com/mui/material-ui",
        note: "focus-trapとaria属性対応済み",
      },
      vue: {
        status: "stable",
        snippet: '<Dialog v-model:visible="visible" modal header="Title">...</Dialog>',
        docs: "https://primevue.org/dialog/",
        source: "https://github.com/primefaces/primevue",
        note: "Portal先の調整が重要",
      },
      svelte: {
        status: "beta",
        snippet: "{#if open}<Modal on:close={close}>...</Modal>{/if}",
        docs: "https://www.skeleton.dev/docs/components/modal",
        source: "https://github.com/skeletonlabs/skeleton",
        note: "状態管理をstore化すると扱いやすい",
      },
      angular: {
        status: "stable",
        snippet: 'this.dialog.open(UserDialogComponent, { width: "480px" });',
        docs: "https://material.angular.io/components/dialog/overview",
        source: "https://github.com/angular/components",
        note: "DialogRefで閉じる値を返せる",
      },
      solid: {
        status: "beta",
        snippet: "<Dialog open={open()} onOpenChange={setOpen}>...</Dialog>",
        docs: "https://www.solid-ui.com/docs/components/dialog",
        source: "https://github.com/kobaltedev/kobalte",
        note: "Kobalte系を使うと実装しやすい",
      },
    },
  },
  {
    id: "toast",
    name: "Toast",
    category: "Feedback",
    description: "非ブロッキングな通知メッセージ表示。",
    preview: "toast",
    tags: ["notification", "message", "feedback"],
    frameworks: {
      react: {
        status: "stable",
        snippet: 'toast.success("Saved successfully");',
        docs: "https://fkhadra.github.io/react-toastify/introduction",
        source: "https://github.com/fkhadra/react-toastify",
        note: "サードパーティ採用が主流",
      },
      vue: {
        status: "stable",
        snippet: 'toast.add({ severity: "success", summary: "Saved" });',
        docs: "https://primevue.org/toast/",
        source: "https://github.com/primefaces/primevue",
        note: "ToastServiceとセットで運用",
      },
      svelte: {
        status: "beta",
        snippet: "toasts.success('Saved successfully');",
        docs: "https://www.skeleton.dev/docs/utilities/toasts",
        source: "https://github.com/skeletonlabs/skeleton",
        note: "store駆動が一般的",
      },
      angular: {
        status: "beta",
        snippet: 'this.snackBar.open("Saved", "Close", { duration: 3000 });',
        docs: "https://material.angular.io/components/snack-bar/overview",
        source: "https://github.com/angular/components",
        note: "SnackBarをToastとして利用",
      },
      solid: {
        status: "planned",
        snippet: "// Planned",
        docs: "",
        source: "",
        note: "通知基盤を調査中",
      },
    },
  },
  {
    id: "tabs",
    name: "Tabs",
    category: "Navigation",
    description: "関連コンテンツをタブで切り替えて表示。",
    preview: "tabs",
    tags: ["navigation", "switch", "panel"],
    frameworks: {
      react: {
        status: "stable",
        snippet: "<Tabs value={value} onChange={handleChange}><Tab label='Overview' /></Tabs>",
        docs: "https://mui.com/material-ui/react-tabs/",
        source: "https://github.com/mui/material-ui",
        note: "アクセシビリティ仕様が明確",
      },
      vue: {
        status: "stable",
        snippet: '<Tabs value="0"><TabList>...</TabList><TabPanels>...</TabPanels></Tabs>',
        docs: "https://primevue.org/tabs/",
        source: "https://github.com/primefaces/primevue",
        note: "テンプレートベースで可読性が高い",
      },
      svelte: {
        status: "beta",
        snippet: "<Tabs bind:value={tab}><Tab value='overview'>Overview</Tab></Tabs>",
        docs: "https://www.skeleton.dev/docs/components/tabs",
        source: "https://github.com/skeletonlabs/skeleton",
        note: "ルーティングと連動させやすい",
      },
      angular: {
        status: "stable",
        snippet: "<mat-tab-group><mat-tab label='Overview'>...</mat-tab></mat-tab-group>",
        docs: "https://material.angular.io/components/tabs/overview",
        source: "https://github.com/angular/components",
        note: "lazy loadingタブも容易",
      },
      solid: {
        status: "planned",
        snippet: "// Planned",
        docs: "",
        source: "",
        note: "既存ヘッドレスUIの採用検討",
      },
    },
  },
  {
    id: "dropdown",
    name: "Dropdown Menu",
    category: "Navigation",
    description: "文脈メニューやナビゲーション補助に使うドロップダウン。",
    preview: "dropdown",
    tags: ["menu", "context", "popover"],
    frameworks: {
      react: {
        status: "stable",
        snippet: "<Menu anchorEl={anchorEl} open={open} onClose={handleClose}>...</Menu>",
        docs: "https://mui.com/material-ui/react-menu/",
        source: "https://github.com/mui/material-ui",
        note: "Popover系と同じ位置計算モデル",
      },
      vue: {
        status: "stable",
        snippet: '<Menu ref="menu" :model="items" popup />',
        docs: "https://primevue.org/menu/",
        source: "https://github.com/primefaces/primevue",
        note: "Overlay表示制御が簡単",
      },
      svelte: {
        status: "beta",
        snippet: "<Dropdown><DropdownItem>Profile</DropdownItem></Dropdown>",
        docs: "https://www.skeleton.dev/docs/components/popover",
        source: "https://github.com/skeletonlabs/skeleton",
        note: "キーボード操作の補完が必要",
      },
      angular: {
        status: "beta",
        snippet: '<button [matMenuTriggerFor]="menu">Open</button><mat-menu #menu="matMenu">...</mat-menu>',
        docs: "https://material.angular.io/components/menu/overview",
        source: "https://github.com/angular/components",
        note: "CDK Overlay依存",
      },
      solid: {
        status: "planned",
        snippet: "// Planned",
        docs: "",
        source: "",
        note: "ヘッドレス実装案を検証中",
      },
    },
  },
  {
    id: "table",
    name: "Table",
    category: "Data Display",
    description: "構造化データを列/行で表示するテーブル。",
    preview: "table",
    tags: ["data", "rows", "columns"],
    frameworks: {
      react: {
        status: "stable",
        snippet: "<Table><TableHead>...</TableHead><TableBody>...</TableBody></Table>",
        docs: "https://mui.com/material-ui/react-table/",
        source: "https://github.com/mui/material-ui",
        note: "高度機能はTanStack Table併用が多い",
      },
      vue: {
        status: "stable",
        snippet: '<DataTable :value="rows"><Column field="name" header="Name" /></DataTable>',
        docs: "https://primevue.org/datatable/",
        source: "https://github.com/primefaces/primevue",
        note: "ページング/ソートが内蔵",
      },
      svelte: {
        status: "beta",
        snippet: "<DataTable {rows} columns={columns} />",
        docs: "https://www.skeleton.dev/",
        source: "https://github.com/skeletonlabs/skeleton",
        note: "ヘッドレス実装比率が高い",
      },
      angular: {
        status: "stable",
        snippet: "<table mat-table [dataSource]='rows'>...</table>",
        docs: "https://material.angular.io/components/table/overview",
        source: "https://github.com/angular/components",
        note: "MatTableDataSourceで簡易導入",
      },
      solid: {
        status: "beta",
        snippet: "<Table data={rows()} columns={columns} />",
        docs: "https://tanstack.com/table/latest/docs/framework/solid/overview",
        source: "https://github.com/TanStack/table",
        note: "TanStack Table採用が中心",
      },
    },
  },
  {
    id: "accordion",
    name: "Accordion",
    category: "Data Display",
    description: "折りたたみ式で情報密度を保ちながら表示するUI。",
    preview: "accordion",
    tags: ["collapse", "faq", "details"],
    frameworks: {
      react: {
        status: "stable",
        snippet: "<Accordion><AccordionSummary>Title</AccordionSummary></Accordion>",
        docs: "https://mui.com/material-ui/react-accordion/",
        source: "https://github.com/mui/material-ui",
        note: "FAQや設定画面でよく利用",
      },
      vue: {
        status: "stable",
        snippet: '<Accordion><AccordionPanel value="0">...</AccordionPanel></Accordion>',
        docs: "https://primevue.org/accordion/",
        source: "https://github.com/primefaces/primevue",
        note: "複数展開モードに対応",
      },
      svelte: {
        status: "stable",
        snippet: "<Accordion><AccordionItem summary='Title'>...</AccordionItem></Accordion>",
        docs: "https://www.skeleton.dev/docs/components/accordion",
        source: "https://github.com/skeletonlabs/skeleton",
        note: "軽量で扱いやすい",
      },
      angular: {
        status: "beta",
        snippet: "<mat-expansion-panel><mat-expansion-panel-header>...</mat-expansion-panel-header></mat-expansion-panel>",
        docs: "https://material.angular.io/components/expansion/overview",
        source: "https://github.com/angular/components",
        note: "Expansion Panelで代替",
      },
      solid: {
        status: "planned",
        snippet: "// Planned",
        docs: "",
        source: "",
        note: "コンポーネント選定中",
      },
    },
  },
  {
    id: "date-picker",
    name: "Date Picker",
    category: "Forms",
    description: "日付選択UI。予約や期限入力などで利用。",
    preview: "calendar",
    tags: ["date", "calendar", "form"],
    frameworks: {
      react: {
        status: "stable",
        snippet: "<DatePicker value={value} onChange={setValue} />",
        docs: "https://mui.com/x/react-date-pickers/",
        source: "https://github.com/mui/mui-x",
        note: "MUI Xで高機能対応",
      },
      vue: {
        status: "stable",
        snippet: '<DatePicker v-model="date" showIcon fluid />',
        docs: "https://primevue.org/datepicker/",
        source: "https://github.com/primefaces/primevue",
        note: "ロケール対応が容易",
      },
      svelte: {
        status: "beta",
        snippet: "<DateInput bind:value={date} />",
        docs: "https://www.skeleton.dev/",
        source: "https://github.com/skeletonlabs/skeleton",
        note: "外部ライブラリ導入率が高い",
      },
      angular: {
        status: "stable",
        snippet: '<input matInput [matDatepicker]="picker"><mat-datepicker #picker></mat-datepicker>',
        docs: "https://material.angular.io/components/datepicker/overview",
        source: "https://github.com/angular/components",
        note: "Material Datepickerが標準",
      },
      solid: {
        status: "planned",
        snippet: "// Planned",
        docs: "",
        source: "",
        note: "実装方式を検証中",
      },
    },
  },
  {
    id: "data-grid",
    name: "Data Grid",
    category: "Data Display",
    description: "大規模データ向けの高機能テーブル（ソート/フィルタ/仮想化）。",
    preview: "grid",
    tags: ["data", "virtualization", "enterprise"],
    frameworks: {
      react: {
        status: "stable",
        snippet: "<DataGrid rows={rows} columns={columns} pagination />",
        docs: "https://mui.com/x/react-data-grid/",
        source: "https://github.com/mui/mui-x",
        note: "最も採用事例が多い",
      },
      vue: {
        status: "beta",
        snippet: '<DataTable :value="rows" paginator :rows="10" scrollable />',
        docs: "https://primevue.org/datatable/",
        source: "https://github.com/primefaces/primevue",
        note: "DataTable拡張で対応可能",
      },
      svelte: {
        status: "planned",
        snippet: "// Planned",
        docs: "",
        source: "",
        note: "仮想化要件を満たす構成を検討中",
      },
      angular: {
        status: "beta",
        snippet: "<ag-grid-angular [rowData]='rows' [columnDefs]='columnDefs'></ag-grid-angular>",
        docs: "https://www.ag-grid.com/angular-data-grid/",
        source: "https://github.com/ag-grid/ag-grid",
        note: "AG Grid採用が一般的",
      },
      solid: {
        status: "planned",
        snippet: "// Planned",
        docs: "",
        source: "",
        note: "実運用候補を評価中",
      },
    },
  },
];

const statusLabelMap = {
  stable: "stable",
  beta: "beta",
  planned: "planned",
};

const state = {
  search: "",
  selectedCategories: new Set(),
  selectedFrameworks: new Set(),
  favorites: new Set(loadFavorites()),
  favoritesOnly: false,
  implementedOnly: false,
  sort: "name",
  compareComponentId: COMPONENTS[0]?.id ?? "",
  compareFrameworks: new Set(DEFAULT_COMPARE_FRAMEWORKS),
  modalComponentId: null,
  modalFrameworkId: null,
};

const els = {};

document.addEventListener("DOMContentLoaded", () => {
  cacheElements();
  bindEvents();
  renderStaticMeta();
  renderFilterChips();
  renderComponentGrid();
  renderCompareControls();
  renderCompareGrid();
});

function cacheElements() {
  els.statComponents = document.getElementById("statComponents");
  els.statFrameworks = document.getElementById("statFrameworks");
  els.statImplementations = document.getElementById("statImplementations");

  els.searchInput = document.getElementById("searchInput");
  els.categoryFilters = document.getElementById("categoryFilters");
  els.frameworkFilters = document.getElementById("frameworkFilters");
  els.favoritesOnlyToggle = document.getElementById("favoritesOnlyToggle");
  els.implementedOnlyToggle = document.getElementById("implementedOnlyToggle");
  els.sortSelect = document.getElementById("sortSelect");
  els.clearFiltersBtn = document.getElementById("clearFiltersBtn");
  els.resultCount = document.getElementById("resultCount");
  els.componentGrid = document.getElementById("componentGrid");
  els.emptyState = document.getElementById("emptyState");

  els.compareComponentSelect = document.getElementById("compareComponentSelect");
  els.compareFrameworkList = document.getElementById("compareFrameworkList");
  els.resetCompareBtn = document.getElementById("resetCompareBtn");
  els.compareGrid = document.getElementById("compareGrid");

  els.detailModal = document.getElementById("detailModal");
  els.modalCloseBtn = document.getElementById("modalCloseBtn");
  els.modalTitle = document.getElementById("modalTitle");
  els.modalDescription = document.getElementById("modalDescription");
  els.modalFrameworkTabs = document.getElementById("modalFrameworkTabs");
  els.modalMeta = document.getElementById("modalMeta");
  els.modalPreview = document.getElementById("modalPreview");
  els.modalCode = document.getElementById("modalCode");
  els.modalLinks = document.getElementById("modalLinks");
  els.copyCodeBtn = document.getElementById("copyCodeBtn");
}

function bindEvents() {
  els.searchInput.addEventListener("input", (event) => {
    state.search = event.target.value.trim().toLowerCase();
    renderComponentGrid();
  });

  els.favoritesOnlyToggle.addEventListener("change", (event) => {
    state.favoritesOnly = Boolean(event.target.checked);
    renderComponentGrid();
  });

  els.implementedOnlyToggle.addEventListener("change", (event) => {
    state.implementedOnly = Boolean(event.target.checked);
    renderComponentGrid();
  });

  els.sortSelect.addEventListener("change", (event) => {
    state.sort = event.target.value;
    renderComponentGrid();
  });

  els.clearFiltersBtn.addEventListener("click", () => {
    state.search = "";
    state.selectedCategories.clear();
    state.selectedFrameworks.clear();
    state.favoritesOnly = false;
    state.implementedOnly = false;
    state.sort = "name";

    els.searchInput.value = "";
    els.favoritesOnlyToggle.checked = false;
    els.implementedOnlyToggle.checked = false;
    els.sortSelect.value = "name";

    renderFilterChips();
    renderComponentGrid();
  });

  els.categoryFilters.addEventListener("click", (event) => {
    const chip = event.target.closest("button[data-category]");
    if (!chip) return;
    const category = chip.dataset.category;
    toggleSetValue(state.selectedCategories, category);
    renderFilterChips();
    renderComponentGrid();
  });

  els.frameworkFilters.addEventListener("click", (event) => {
    const chip = event.target.closest("button[data-framework]");
    if (!chip) return;
    const frameworkId = chip.dataset.framework;
    toggleSetValue(state.selectedFrameworks, frameworkId);
    renderFilterChips();
    renderComponentGrid();
  });

  els.componentGrid.addEventListener("click", (event) => {
    const actionTarget = event.target.closest("button[data-action]");
    if (!actionTarget) return;

    const action = actionTarget.dataset.action;
    const componentId = actionTarget.dataset.componentId;
    if (!componentId) return;

    if (action === "favorite") {
      toggleFavorite(componentId);
      renderComponentGrid();
      return;
    }

    if (action === "detail") {
      openModal(componentId);
      return;
    }

    if (action === "compare") {
      state.compareComponentId = componentId;
      els.compareComponentSelect.value = componentId;
      renderCompareGrid();
      document.getElementById("compare")?.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  });

  els.compareComponentSelect.addEventListener("change", (event) => {
    state.compareComponentId = event.target.value;
    renderCompareGrid();
  });

  els.compareFrameworkList.addEventListener("change", (event) => {
    const target = event.target;
    if (!(target instanceof HTMLInputElement) || !target.dataset.frameworkId) return;
    if (target.checked) {
      state.compareFrameworks.add(target.dataset.frameworkId);
    } else {
      state.compareFrameworks.delete(target.dataset.frameworkId);
    }
    renderCompareGrid();
  });

  els.resetCompareBtn.addEventListener("click", () => {
    state.compareComponentId = COMPONENTS[0]?.id ?? "";
    state.compareFrameworks = new Set(DEFAULT_COMPARE_FRAMEWORKS);
    renderCompareControls();
    renderCompareGrid();
  });

  els.modalCloseBtn.addEventListener("click", closeModal);
  els.detailModal.addEventListener("click", (event) => {
    if (event.target instanceof HTMLElement && event.target.hasAttribute("data-close-modal")) {
      closeModal();
    }
  });

  els.modalFrameworkTabs.addEventListener("click", (event) => {
    const tab = event.target.closest("button[data-framework-id]");
    if (!tab) return;
    state.modalFrameworkId = tab.dataset.frameworkId;
    renderModalBody();
  });

  els.copyCodeBtn.addEventListener("click", copyModalCode);

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && els.detailModal.classList.contains("is-open")) {
      closeModal();
    }
  });
}

function renderStaticMeta() {
  const implementationCount = COMPONENTS.reduce((total, component) => {
    return total + getImplementedCount(component);
  }, 0);

  els.statComponents.textContent = String(COMPONENTS.length);
  els.statFrameworks.textContent = String(FRAMEWORKS.length);
  els.statImplementations.textContent = String(implementationCount);
}

function renderFilterChips() {
  const categories = Array.from(new Set(COMPONENTS.map((component) => component.category))).sort((a, b) =>
    a.localeCompare(b)
  );

  els.categoryFilters.innerHTML = categories
    .map((category) => {
      const active = state.selectedCategories.has(category);
      return `<button type="button" class="chip ${active ? "is-active" : ""}" data-category="${escapeHtml(
        category
      )}">${escapeHtml(category)}</button>`;
    })
    .join("");

  els.frameworkFilters.innerHTML = FRAMEWORKS.map((framework) => {
    const active = state.selectedFrameworks.has(framework.id);
    return `<button type="button" class="chip ${active ? "is-active" : ""}" data-framework="${framework.id}">${framework.label}</button>`;
  }).join("");
}

function renderComponentGrid() {
  const components = getFilteredComponents();

  els.resultCount.textContent = `${components.length} components`;
  els.componentGrid.innerHTML = components.map((component) => buildComponentCard(component)).join("");
  els.emptyState.classList.toggle("hidden", components.length > 0);
}

function getFilteredComponents() {
  const filtered = COMPONENTS.filter((component) => {
    if (state.search) {
      const content = [component.name, component.description, component.category, ...component.tags]
        .join(" ")
        .toLowerCase();
      if (!content.includes(state.search)) return false;
    }

    if (state.selectedCategories.size && !state.selectedCategories.has(component.category)) {
      return false;
    }

    if (state.selectedFrameworks.size) {
      const hasAnyMatchedFramework = Array.from(state.selectedFrameworks).some((frameworkId) =>
        isImplemented(getFrameworkEntry(component, frameworkId).status)
      );
      if (!hasAnyMatchedFramework) return false;
    }

    if (state.favoritesOnly && !state.favorites.has(component.id)) {
      return false;
    }

    if (state.implementedOnly) {
      const hasPlannedImplementation = FRAMEWORK_ORDER.some(
        (frameworkId) => getFrameworkEntry(component, frameworkId).status === "planned"
      );
      if (hasPlannedImplementation) return false;
    }

    return true;
  });

  filtered.sort((left, right) => {
    if (state.sort === "coverage") {
      const coverageDiff = getImplementedCount(right) - getImplementedCount(left);
      if (coverageDiff !== 0) return coverageDiff;
      return left.name.localeCompare(right.name);
    }

    if (state.sort === "category") {
      const categoryDiff = left.category.localeCompare(right.category);
      if (categoryDiff !== 0) return categoryDiff;
      return left.name.localeCompare(right.name);
    }

    return left.name.localeCompare(right.name);
  });

  return filtered;
}

function buildComponentCard(component) {
  const favoriteActive = state.favorites.has(component.id);
  const implementedCount = getImplementedCount(component);
  const coverageStatus = getCoverageStatus(component);
  const frameworkBadges = FRAMEWORK_ORDER.map((frameworkId) => {
    const framework = getFrameworkById(frameworkId);
    const entry = getFrameworkEntry(component, frameworkId);
    return `<span class="framework-badge" data-status="${entry.status}">${framework.label}</span>`;
  }).join("");

  return `
    <article class="component-card">
      ${buildPreview(component.preview)}
      <div class="card-body">
        <div class="card-head">
          <div>
            <h3>${escapeHtml(component.name)}</h3>
          </div>
          <button
            type="button"
            class="favorite-btn ${favoriteActive ? "is-active" : ""}"
            data-action="favorite"
            data-component-id="${component.id}"
            aria-label="${favoriteActive ? "お気に入り解除" : "お気に入り登録"}"
          >${favoriteActive ? "★" : "☆"}</button>
        </div>

        <p class="card-desc">${escapeHtml(component.description)}</p>

        <div class="card-meta">
          <span class="tag">${escapeHtml(component.category)}</span>
          <span class="status status--${coverageStatus}">
            ${implementedCount}/${FRAMEWORKS.length} implemented
          </span>
        </div>

        <div class="framework-list">${frameworkBadges}</div>

        <div class="card-actions">
          <button class="btn btn--primary btn--sm" type="button" data-action="detail" data-component-id="${component.id}">
            詳細
          </button>
          <button class="btn btn--ghost btn--sm" type="button" data-action="compare" data-component-id="${component.id}">
            比較
          </button>
        </div>
      </div>
    </article>
  `;
}

function renderCompareControls() {
  els.compareComponentSelect.innerHTML = COMPONENTS.map((component) => {
    return `<option value="${component.id}">${escapeHtml(component.name)}</option>`;
  }).join("");
  els.compareComponentSelect.value = state.compareComponentId;

  els.compareFrameworkList.innerHTML = FRAMEWORKS.map((framework) => {
    const checked = state.compareFrameworks.has(framework.id) ? "checked" : "";
    return `
      <label class="checkbox-item">
        <input type="checkbox" data-framework-id="${framework.id}" ${checked}>
        <span>${framework.label}</span>
      </label>
    `;
  }).join("");
}

function renderCompareGrid() {
  const component = getComponentById(state.compareComponentId) ?? COMPONENTS[0];
  if (!component) {
    els.compareGrid.innerHTML = "";
    return;
  }

  const selectedFrameworks = FRAMEWORK_ORDER.filter((frameworkId) => state.compareFrameworks.has(frameworkId));
  if (!selectedFrameworks.length) {
    els.compareGrid.innerHTML = `
      <div class="empty-state">
        <h3>比較対象が選択されていません</h3>
        <p>少なくとも1つのフレームワークを選択してください。</p>
      </div>
    `;
    return;
  }

  els.compareGrid.innerHTML = selectedFrameworks
    .map((frameworkId) => {
      const framework = getFrameworkById(frameworkId);
      const entry = getFrameworkEntry(component, frameworkId);
      const snippet = isImplemented(entry.status)
        ? entry.snippet
        : `// ${framework.label} implementation is planned`;

      const links = [
        entry.docs ? `<a href="${entry.docs}" target="_blank" rel="noopener noreferrer">Docs</a>` : "",
        entry.source ? `<a href="${entry.source}" target="_blank" rel="noopener noreferrer">Source</a>` : "",
      ]
        .filter(Boolean)
        .join(" ");

      return `
        <article class="compare-card">
          <div class="compare-card__head">
            <strong>${framework.label}</strong>
            <span class="status status--${entry.status}">${statusLabelMap[entry.status]}</span>
          </div>
          <div class="compare-card__body">
            <p class="compare-card__note">${escapeHtml(entry.note || "補足情報なし")}</p>
            <pre class="code-block"><code>${escapeHtml(snippet)}</code></pre>
            <div class="modal__links">${links || '<span class="tag">リンクなし</span>'}</div>
          </div>
        </article>
      `;
    })
    .join("");
}

function openModal(componentId) {
  const component = getComponentById(componentId);
  if (!component) return;

  state.modalComponentId = componentId;
  const implementedFramework = FRAMEWORK_ORDER.find((frameworkId) =>
    isImplemented(getFrameworkEntry(component, frameworkId).status)
  );
  state.modalFrameworkId = implementedFramework ?? FRAMEWORK_ORDER[0];

  renderModalBody();
  els.detailModal.classList.add("is-open");
  els.detailModal.setAttribute("aria-hidden", "false");
  document.body.style.overflow = "hidden";
}

function closeModal() {
  els.detailModal.classList.remove("is-open");
  els.detailModal.setAttribute("aria-hidden", "true");
  document.body.style.overflow = "";
}

function renderModalBody() {
  const component = getComponentById(state.modalComponentId);
  if (!component) return;

  const frameworkId = state.modalFrameworkId ?? FRAMEWORK_ORDER[0];
  const framework = getFrameworkById(frameworkId);
  const entry = getFrameworkEntry(component, frameworkId);
  const implementedCount = getImplementedCount(component);
  const snippet = isImplemented(entry.status)
    ? entry.snippet
    : `// ${framework.label} implementation is planned`;

  els.modalTitle.textContent = component.name;
  els.modalDescription.textContent = component.description;
  els.modalFrameworkTabs.innerHTML = FRAMEWORK_ORDER.map((id) => {
    const currentEntry = getFrameworkEntry(component, id);
    const active = frameworkId === id;
    const buttonClassName = active ? "tab-btn is-active" : "tab-btn";
    const frameworkLabel = getFrameworkById(id).label;

    return `
      <button
        type="button"
        class="${buttonClassName}"
        data-framework-id="${id}"
        role="tab"
        aria-selected="${active ? "true" : "false"}"
      >
        ${frameworkLabel}
        <span class="status status--${currentEntry.status}">${statusLabelMap[currentEntry.status]}</span>
      </button>
    `;
  }).join("");

  els.modalMeta.innerHTML = `
    <span class="tag">${escapeHtml(component.category)}</span>
    <span class="tag">${implementedCount}/${FRAMEWORKS.length} implemented</span>
    ${component.tags.map((tag) => `<span class="tag">#${escapeHtml(tag)}</span>`).join("")}
  `;
  els.modalPreview.innerHTML = buildPreview(component.preview);
  els.modalCode.textContent = snippet;

  const links = [
    entry.docs ? `<a href="${entry.docs}" target="_blank" rel="noopener noreferrer">公式ドキュメント</a>` : "",
    entry.source ? `<a href="${entry.source}" target="_blank" rel="noopener noreferrer">GitHub</a>` : "",
  ]
    .filter(Boolean)
    .join("");
  els.modalLinks.innerHTML = links || '<span class="tag">このフレームワークの外部リンクは未登録です</span>';
}

async function copyModalCode() {
  const code = els.modalCode.textContent;
  if (!code) return;

  const originalText = els.copyCodeBtn.textContent;
  try {
    if (!navigator.clipboard || !navigator.clipboard.writeText) {
      throw new Error("Clipboard API unavailable");
    }
    await navigator.clipboard.writeText(code);
    els.copyCodeBtn.textContent = "コピーしました";
  } catch (error) {
    // Fallback: selection-based copy for environments without Clipboard API.
    const range = document.createRange();
    range.selectNodeContents(els.modalCode);
    const selection = window.getSelection();
    selection?.removeAllRanges();
    selection?.addRange(range);
    document.execCommand("copy");
    selection?.removeAllRanges();
    els.copyCodeBtn.textContent = "コピーしました";
  }

  window.setTimeout(() => {
    els.copyCodeBtn.textContent = originalText;
  }, 1300);
}

function toggleFavorite(componentId) {
  if (state.favorites.has(componentId)) {
    state.favorites.delete(componentId);
  } else {
    state.favorites.add(componentId);
  }
  persistFavorites(state.favorites);
}

function getFrameworkById(frameworkId) {
  return FRAMEWORKS.find((framework) => framework.id === frameworkId);
}

function getComponentById(componentId) {
  return COMPONENTS.find((component) => component.id === componentId);
}

function getFrameworkEntry(component, frameworkId) {
  const value = component.frameworks[frameworkId];
  if (value) return value;
  return {
    status: "planned",
    snippet: "// Planned",
    docs: "",
    source: "",
    note: "未対応",
  };
}

function getImplementedCount(component) {
  return FRAMEWORK_ORDER.reduce((count, frameworkId) => {
    const status = getFrameworkEntry(component, frameworkId).status;
    return isImplemented(status) ? count + 1 : count;
  }, 0);
}

function getCoverageStatus(component) {
  const implementedCount = getImplementedCount(component);
  if (implementedCount >= FRAMEWORKS.length) return "stable";
  if (implementedCount >= Math.ceil(FRAMEWORKS.length / 2)) return "beta";
  return "planned";
}

function isImplemented(status) {
  return status === "stable" || status === "beta";
}

function toggleSetValue(set, value) {
  if (set.has(value)) {
    set.delete(value);
  } else {
    set.add(value);
  }
}

function loadFavorites() {
  try {
    const raw = localStorage.getItem(FAVORITES_STORAGE_KEY);
    if (!raw) return [];
    const parsed = JSON.parse(raw);
    return Array.isArray(parsed) ? parsed : [];
  } catch {
    return [];
  }
}

function persistFavorites(favoritesSet) {
  try {
    localStorage.setItem(FAVORITES_STORAGE_KEY, JSON.stringify(Array.from(favoritesSet)));
  } catch {
    // Ignore storage errors in private mode or restricted environments.
  }
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

function buildPreview(type) {
  if (type === "button" || type === "icon-button") {
    return `
      <div class="preview preview--button">
        <div class="preview__row">
          <span class="preview__pill big"></span>
          <span class="preview__pill small"></span>
        </div>
        <span class="preview__line mid"></span>
      </div>
    `;
  }

  if (type === "input" || type === "select" || type === "calendar") {
    return `
      <div class="preview preview--form">
        <span class="preview__line wide"></span>
        <span class="preview__line mid"></span>
        <span class="preview__line short"></span>
      </div>
    `;
  }

  if (type === "table" || type === "grid") {
    return `
      <div class="preview preview--table">
        <div class="preview__table">
          <span class="preview__line wide"></span>
          <span class="preview__line mid"></span>
          <span class="preview__line wide"></span>
        </div>
      </div>
    `;
  }

  if (type === "tabs" || type === "dropdown" || type === "accordion") {
    return `
      <div class="preview preview--nav">
        <div class="preview__row">
          <span class="preview__pill small"></span>
          <span class="preview__pill small"></span>
          <span class="preview__pill small"></span>
        </div>
        <span class="preview__line wide"></span>
      </div>
    `;
  }

  if (type === "toast" || type === "modal") {
    return `
      <div class="preview preview--feedback">
        <span class="preview__line wide"></span>
        <span class="preview__line mid"></span>
        <span class="preview__line short"></span>
      </div>
    `;
  }

  return `
    <div class="preview">
      <span class="preview__line wide"></span>
      <span class="preview__line mid"></span>
      <span class="preview__line short"></span>
    </div>
  `;
}
