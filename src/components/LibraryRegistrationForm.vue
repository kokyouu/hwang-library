<template>
  <div class="container mt-5">
    <div class="row">
      <div class="col-md-8 offset-md-2">
        <h1 class="text-center mb-2">
          🗄️ W5. Library Registration Form
        </h1>

        <p class="text-center mb-4">
          Let's build some more advanced features into our form.
        </p>

        <form
          @submit.prevent="submitForm"
          novalidate
        >
          <!-- Row 1: Username and Gender -->
          <div class="row mb-3">
            <div class="col-md-6 col-sm-6">
              <label
                for="username"
                class="form-label"
              >
                Username
              </label>

              <input
                id="username"
                v-model="formData.username"
                type="text"
                class="form-control"
                :class="{ 'is-invalid': errors.username }"
                @blur="() => validateName(true)"
                @input="() => validateName(false)"
              />

              <div
                v-if="errors.username"
                class="text-danger validation-message"
              >
                {{ errors.username }}
              </div>
            </div>

            <div class="col-md-6 col-sm-6">
              <label
                for="gender"
                class="form-label"
              >
                Gender
              </label>

              <select
                id="gender"
                v-model="formData.gender"
                class="form-select"
                :class="{ 'is-invalid': errors.gender }"
                @blur="() => validateGender(true)"
                @change="() => validateGender(true)"
              >
                <option
                  disabled
                  value=""
                >
                  Please select a gender
                </option>

                <option value="male">
                  Male
                </option>

                <option value="female">
                  Female
                </option>

                <option value="other">
                  Other
                </option>
              </select>

              <div
                v-if="errors.gender"
                class="text-danger validation-message"
              >
                {{ errors.gender }}
              </div>
            </div>
          </div>

          <!-- Row 2: Password and Confirm Password -->
          <div class="row mb-3">
            <div class="col-md-6 col-sm-6">
              <label
                for="password"
                class="form-label"
              >
                Password
              </label>

              <input
                id="password"
                v-model="formData.password"
                type="password"
                class="form-control"
                :class="{ 'is-invalid': errors.password }"
                @blur="() => validatePassword(true)"
                @input="() => validatePassword(false)"
              />

              <div
                v-if="errors.password"
                class="text-danger validation-message"
              >
                {{ errors.password }}
              </div>
            </div>

            <div class="col-md-6 col-sm-6">
              <label
                for="confirm-password"
                class="form-label"
              >
                Confirm password
              </label>

              <input
                id="confirm-password"
                v-model="formData.confirmPassword"
                type="password"
                class="form-control"
                :class="{
                  'is-invalid': errors.confirmPassword
                }"
                @blur="() => validateConfirmPassword(true)"
              />

              <div
                v-if="errors.confirmPassword"
                class="text-danger validation-message"
              >
                {{ errors.confirmPassword }}
              </div>
            </div>
          </div>

          <!-- Australian Resident -->
          <div class="mb-3">
            <div class="form-check">
              <input
                id="isAustralian"
                v-model="formData.isAustralian"
                type="checkbox"
                class="form-check-input"
                :class="{ 'is-invalid': errors.resident }"
                @change="() => validateResident(true)"
              />

              <label
                for="isAustralian"
                class="form-check-label"
              >
                Australian Resident?
              </label>
            </div>

            <div
              v-if="errors.resident"
              class="text-danger validation-message"
            >
              {{ errors.resident }}
            </div>
          </div>

          <!-- Reason -->
          <div class="mb-3">
            <label
              for="reason"
              class="form-label"
            >
              Reason for joining
            </label>

            <textarea
              id="reason"
              v-model="formData.reason"
              class="form-control"
              :class="{ 'is-invalid': errors.reason }"
              rows="3"
              @blur="() => validateReason(true)"
              @input="() => validateReason(false)"
            ></textarea>

            <div class="d-flex justify-content-between">
              <div
                v-if="errors.reason"
                class="text-danger validation-message"
              >
                {{ errors.reason }}
              </div>

              <span class="ms-auto text-muted">
                {{ formData.reason.length }}/200
              </span>
            </div>
          </div>

          <!-- Buttons -->
          <div class="text-center">
            <button
              type="submit"
              class="btn btn-primary me-2"
            >
              Submit
            </button>

            <button
              type="button"
              class="btn btn-secondary"
              @click="clearForm"
            >
              Clear
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- PrimeVue DataTable -->
    <section class="mt-5">
      <h2 class="mb-3">
        This is a PrimeVue DataTable.
      </h2>

      <div class="table-responsive">
        <DataTable
          :value="submittedCards"
          data-key="id"
          show-gridlines
          striped-rows
          table-style="min-width: 50rem"
        >
          <Column
            field="username"
            header="Username"
          />

          <Column
            field="password"
            header="Password"
          />

          <Column
            header="Australian Resident"
          >
            <template #body="{ data }">
              {{ data.isAustralian ? 'Yes' : 'No' }}
            </template>
          </Column>

          <Column
            field="gender"
            header="Gender"
          />

          <Column
            field="reason"
            header="Reason"
          />
        </DataTable>
      </div>
    </section>

    <!-- Bootstrap Cards -->
    <section
      v-if="submittedCards.length > 0"
      class="d-flex flex-wrap mt-4"
    >
      <div
        v-for="card in submittedCards"
        :key="card.id"
        class="card user-card me-3 mb-3"
      >
        <div class="card-header">
          User Information
        </div>

        <ul class="list-group list-group-flush">
          <li class="list-group-item">
            Username: {{ card.username }}
          </li>

          <li class="list-group-item">
            Password: {{ card.password }}
          </li>

          <li class="list-group-item">
            Australian Resident:
            {{ card.isAustralian ? 'Yes' : 'No' }}
          </li>

          <li class="list-group-item">
            Gender: {{ card.gender }}
          </li>

          <li class="list-group-item">
            Reason: {{ card.reason }}
          </li>
        </ul>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'

const formData = ref({
  username: '',
  password: '',
  confirmPassword: '',
  isAustralian: false,
  reason: '',
  gender: ''
})

const errors = ref({
  username: null,
  password: null,
  confirmPassword: null,
  resident: null,
  gender: null,
  reason: null
})

const submittedCards = ref([])

let nextId = 1

const validateName = (blur) => {
  const username = formData.value.username.trim()

  if (username.length < 3) {
    if (blur) {
      errors.value.username =
        'Name must be at least 3 characters.'
    }

    return false
  }

  errors.value.username = null
  return true
}

const validatePassword = (blur) => {
  const password = formData.value.password

  const hasUppercase = /[A-Z]/.test(password)
  const hasLowercase = /[a-z]/.test(password)
  const hasNumber = /\d/.test(password)
  const hasSpecialCharacter =
    /[!@#$%^&*(),.?":{}|<>]/.test(password)

  let message = null

  if (password.length < 8) {
    message =
      'Password must be at least 8 characters long.'
  } else if (!hasUppercase) {
    message =
      'Password must contain an uppercase letter.'
  } else if (!hasLowercase) {
    message =
      'Password must contain a lowercase letter.'
  } else if (!hasNumber) {
    message =
      'Password must contain a number.'
  } else if (!hasSpecialCharacter) {
    message =
      'Password must contain a special character.'
  }

  if (message) {
    if (blur) {
      errors.value.password = message
    }

    return false
  }

  errors.value.password = null
  return true
}

/**
 * Checks whether Password and Confirm Password match.
 * Validation is displayed when Confirm Password loses focus.
 */
const validateConfirmPassword = (blur) => {
  if (
    formData.value.password !==
    formData.value.confirmPassword
  ) {
    if (blur) {
      errors.value.confirmPassword =
        'Passwords do not match.'
    }

    return false
  }

  errors.value.confirmPassword = null
  return true
}

const validateResident = (blur) => {
  if (!formData.value.isAustralian) {
    if (blur) {
      errors.value.resident =
        'Please confirm your Australian resident status.'
    }

    return false
  }

  errors.value.resident = null
  return true
}

const validateGender = (blur) => {
  if (!formData.value.gender) {
    if (blur) {
      errors.value.gender =
        'Please select a gender.'
    }

    return false
  }

  errors.value.gender = null
  return true
}

const validateReason = (blur) => {
  const reason = formData.value.reason.trim()

  let message = null

  if (reason.length < 10) {
    message =
      'Reason must be at least 10 characters.'
  } else if (reason.length > 200) {
    message =
      'Reason must not exceed 200 characters.'
  }

  if (message) {
    if (blur) {
      errors.value.reason = message
    }

    return false
  }

  errors.value.reason = null
  return true
}

const submitForm = () => {
  validateName(true)
  validatePassword(true)
  validateConfirmPassword(true)
  validateResident(true)
  validateGender(true)
  validateReason(true)

  const hasErrors = Object.values(
    errors.value
  ).some((error) => error !== null)

  if (hasErrors) {
    return
  }

  submittedCards.value.push({
    id: nextId,
    username: formData.value.username.trim(),
    password: formData.value.password,
    isAustralian: formData.value.isAustralian,
    gender: formData.value.gender,
    reason: formData.value.reason.trim()
  })

  nextId += 1
  clearForm()
}

const clearForm = () => {
  formData.value = {
    username: '',
    password: '',
    confirmPassword: '',
    isAustralian: false,
    reason: '',
    gender: ''
  }

  errors.value = {
    username: null,
    password: null,
    confirmPassword: null,
    resident: null,
    gender: null,
    reason: null
  }
}
</script>

<style scoped>
.validation-message {
  margin-top: 0.25rem;
  font-size: 0.875rem;
}

.user-card {
  width: 18rem;
}

.card-header {
  background-color: #3156d9;
  color: white;
}
</style>