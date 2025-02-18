<script>
export default {
  name: 'DynamicForm',
  props: {
    value: {
      type: Object,
      required: true,
    },
    readonly: {
      type: Boolean,
      default: false,
    }
  },
  data() {
    return {
      collapsed: {},
    }
  },
  methods: {
    updateValue(key, newValue) {
      this.$emit('update:value', { ...this.value, [key]: newValue })
    },
    updateNestedValue(key, updatedValue) {
      this.$emit('update:value', { ...this.value, [key]: updatedValue })
    },
    toggleCollapse(key) {
      this.collapsed[key] = !this.collapsed[key];
    }
  },
  watch: {
    value: {
      immediate: true,
      handler(newVal) {
        for (const key in newVal) {
          if (typeof newVal[key] === 'object' && newVal[key] !== null) {
            if (this.collapsed[key] === undefined) {
              this.collapsed[key] = true;
            }
          }
        }
      }
    }
  },
}
</script>

<template>
  <div v-for="(value, key) in value" :key="key" class="w-100">

    <hr v-if="!$parent || $parent.$options.name !== 'DynamicForm'" style="height: 2px; background-color: black; border: none; margin: 20px 0;" />

    <label class="form-label">
      {{ key }}:
    </label>

    <div v-if="typeof value === 'object' && value !== null" class="inputs-row">
      <button type="button" @click="toggleCollapse(key)" class="btn btn-light btn-outline-dark">
        {{ collapsed[key] ? 'Rozwiń' : 'Zwiń' }}
      </button>
      <div v-show="!collapsed[key]">
        <DynamicForm :value="value" @update:value="updateNestedValue(key, $event)" />
      </div>
    </div>

    <input
      v-else
      :value="value"
      @input="updateValue(key, $event.target.value)"
      :placeholder="key"
      :name="key"
      :readonly="readonly"
      type="text"
      class="form-control"
    />
  </div>
</template>
