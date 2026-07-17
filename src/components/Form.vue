<template>
  <div class="container py-5">
    <div class="row">
      <div class="col-lg-10 col-xl-8 mx-auto">
        <h1 class="text-center mb-4">User Information Form</h1>

        <!-- novalidate disables browser-native validation.
             This allows Vue validation messages to be displayed. -->
        <form @submit.prevent="submitForm" novalidate>
          <!-- Username and Password -->
          <div class="row mb-3">
            <!-- Username -->
            <div class="col-md-6 col-sm-12 mb-3 mb-md-0">
              <label for="username" class="form-label">
                Username
              </label>

              <input
                id="username"
                v-model="formData.username"
                type="text"
                class="form-control"
                :class="{ 'is-invalid': errors.username }"
                @blur="validateName(true)"
                @input="validateName(false)"
              />

              <div
                v-if="errors.username"
                class="text-danger validation-message"
              >
                {{ errors.username }}
              </div>
            </div>

            <!-- Password -->
            <div class="col-md-6 col-sm-12">
              <label for="password" class="form-label">
                Password
              </label>

              <input
                id="password"
                v-model="formData.password"
                type="password"
                class="form-control"
                :class="{ 'is-invalid': errors.password }"
                autocomplete="new-password"
                @blur="validatePassword(true)"
                @input="validatePassword(false)"
              />

              <div
                v-if="errors.password"
                class="text-danger validation-message"
              >
                {{ errors.password }}
              </div>
            </div>
          </div>

          <!-- Resident and Gender -->
          <div class="row mb-3">
            <!-- Australian Resident -->
            <div class="col-md-6 col-sm-12 mb-3 mb-md-0">
              <div class="form-check resident-checkbox">
                <input
                  id="isAustralian"
                  v-model="formData.isAustralian"
                  type="checkbox"
                  class="form-check-input"
                  :class="{ 'is-invalid': errors.isAustralian }"
                  @change="validateResident(true)"
                />

                <label
                  class="form-check-label"
                  for="isAustralian"
                >
                  Australian Resident?
                </label>
              </div>

              <div
                v-if="errors.isAustralian"
                class="text-danger validation-message"
              >
                {{ errors.isAustralian }}
              </div>
            </div>

            <!-- Gender -->
            <div class="col-md-6 col-sm-12">
              <label for="gender" class="form-label">
                Gender
              </label>

              <select
                id="gender"
                v-model="formData.gender"
                class="form-select"
                :class="{ 'is-invalid': errors.gender }"
                @blur="validateGender(true)"
                @change="validateGender(true)"
              >
                <option disabled value="">
                  Please select a gender
                </option>
                <option value="male">Male</option>
                <option value="female">Female</option>
                <option value="other">Other</option>
              </select>

              <div
                v-if="errors.gender"
                class="text-danger validation-message"
              >
                {{ errors.gender }}
              </div>
            </div>
          </div>

          <!-- Reason -->
          <div class="mb-3">
            <label for="reason" class="form-label">
              Reason for joining
            </label>

            <textarea
              id="reason"
              v-model="formData.reason"
              class="form-control"
              :class="{ 'is-invalid': errors.reason }"
              rows="3"
              @blur="validateReason(true)"
              @input="validateReason(false)"
            ></textarea>

            <div class="d-flex justify-content-between">
              <div
                v-if="errors.reason"
                class="text-danger validation-message"
              >
                {{ errors.reason }}
              </div>

              <div
                class="form-text ms-auto"
                :class="{ 'text-danger': formData.reason.length > 200 }"
              >
                {{ formData.reason.length }}/200
              </div>
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
    <div
      v-if="submittedUsers.length > 0"
      class="row mt-5"
    >
      <div class="col-12">
        <h2 class="text-center mb-4">
          Submitted User Information
        </h2>

        <div class="table-wrapper">
          <DataTable
            :value="submittedUsers"
            dataKey="id"
            paginator
            :rows="5"
            stripedRows
            showGridlines
            tableStyle="min-width: 50rem"
          >
            <Column
              field="username"
              header="Username"
              sortable
            />

            <Column
              field="password"
              header="Password"
            />

            <Column
              header="Australian Resident"
              sortable
              sortField="isAustralian"
            >
              <template #body="{ data }">
                {{ data.isAustralian ? 'Yes' : 'No' }}
              </template>
            </Column>

            <Column
              field="gender"
              header="Gender"
              sortable
            >
              <template #body="{ data }">
                {{ formatGender(data.gender) }}
              </template>
            </Column>

            <Column
              field="reason"
              header="Reason"
            />
          </DataTable>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'

/*
 * Returns a new empty object each time.
 * This prevents old submitted records from being accidentally modified
 * when the form is cleared.
 */
const createEmptyForm = () => ({
  username: '',
  password: '',
  isAustralian: false,
  gender: '',
  reason: ''
})

const formData = ref(createEmptyForm())

const submittedUsers = ref([])

let nextId = 1

/*
 * Each property stores either:
 * - null: no error
 * - string: error message
 */
const errors = ref({
  username: null,
  password: null,
  isAustralian: null,
  gender: null,
  reason: null
})

/*
 * Validation 1: Username
 * Requirement: at least 3 characters.
 */
const validateName = (showError = true) => {
  const username = formData.value.username.trim()

  if (username.length < 3) {
    /*
     * On blur or submit, show the error immediately.
     * During input, update the message only if an error
     * was already displayed.
     */
    if (showError || errors.value.username) {
      errors.value.username =
        'Name must be at least 3 characters.'
    }

    return false
  }

  errors.value.username = null
  return true
}

/*
 * Validation 2: Password
 * Requirements:
 * - at least 8 characters
 * - at least one uppercase letter
 * - at least one lowercase letter
 * - at least one number
 * - at least one special character
 */
const validatePassword = (showError = true) => {
  const password = formData.value.password
  const minLength = 8

  const hasUppercase = /[A-Z]/.test(password)
  const hasLowercase = /[a-z]/.test(password)
  const hasNumber = /\d/.test(password)
  const hasSpecialCharacter =
    /[!@#$%^&*(),.?":{}|<>]/.test(password)

  let message = null

  if (password.length < minLength) {
    message =
      `Password must be at least ${minLength} characters long.`
  } else if (!hasUppercase) {
    message =
      'Password must contain at least one uppercase letter.'
  } else if (!hasLowercase) {
    message =
      'Password must contain at least one lowercase letter.'
  } else if (!hasNumber) {
    message =
      'Password must contain at least one number.'
  } else if (!hasSpecialCharacter) {
    message =
      'Password must contain at least one special character.'
  }

  if (message) {
    if (showError || errors.value.password) {
      errors.value.password = message
    }

    return false
  }

  errors.value.password = null
  return true
}

/*
 * Validation 3: Australian Resident
 *
 * For this assessed lab, the checkbox must be selected.
 * In a real application, Yes/No radio buttons would normally
 * be better because "No" can also be a valid answer.
 */
const validateResident = (showError = true) => {
  if (!formData.value.isAustralian) {
    if (showError || errors.value.isAustralian) {
      errors.value.isAustralian =
        'Please confirm your Australian resident status.'
    }

    return false
  }

  errors.value.isAustralian = null
  return true
}

/*
 * Validation 4: Gender
 * Requirement: one option must be selected.
 */
const validateGender = (showError = true) => {
  if (!formData.value.gender) {
    if (showError || errors.value.gender) {
      errors.value.gender =
        'Please select a gender.'
    }

    return false
  }

  errors.value.gender = null
  return true
}

/*
 * Validation 5: Reason
 * Requirements:
 * - cannot be empty
 * - at least 10 characters
 * - no more than 200 characters
 */
const validateReason = (showError = true) => {
  const reason = formData.value.reason.trim()

  let message = null

  if (reason.length === 0) {
    message =
      'Please enter a reason for joining.'
  } else if (reason.length < 10) {
    message =
      'Reason must be at least 10 characters.'
  } else if (reason.length > 200) {
    message =
      'Reason must not exceed 200 characters.'
  }

  if (message) {
    if (showError || errors.value.reason) {
      errors.value.reason = message
    }

    return false
  }

  errors.value.reason = null
  return true
}

/*
 * Validate all five groups before adding a record.
 */
const submitForm = () => {
  const validationResults = [
    validateName(true),
    validatePassword(true),
    validateResident(true),
    validateGender(true),
    validateReason(true)
  ]

  const formIsValid =
    validationResults.every((result) => result)

  if (!formIsValid) {
    return
  }

  /*
   * Use a copied object rather than storing the formData object
   * directly. Otherwise clearing the form could also clear
   * previously submitted rows.
   */
  submittedUsers.value.push({
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

/*
 * Clear current input and validation errors.
 * Submitted table records are preserved.
 */
const clearForm = () => {
  formData.value = createEmptyForm()

  errors.value = {
    username: null,
    password: null,
    isAustralian: null,
    gender: null,
    reason: null
  }
}

const formatGender = (gender) => {
  if (!gender) {
    return ''
  }

  return gender.charAt(0).toUpperCase() + gender.slice(1)
}
</script>

<style scoped>
.validation-message {
  margin-top: 0.25rem;
  font-size: 0.875rem;
}

.resident-checkbox {
  margin-top: 2rem;
}

.table-wrapper {
  overflow-x: auto;
}

@media (max-width: 767.98px) {
  .resident-checkbox {
    margin-top: 0;
  }
}
</style>