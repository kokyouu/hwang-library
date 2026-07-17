<template>
  <div class="container mt-5">
    <!-- User Information Form -->
    <div class="row">
      <div class="col-md-8 offset-md-2">
        <h1 class="text-center mb-4">
          User Information Form
        </h1>

        <form @submit.prevent="submitForm">
          <!-- Username and Password -->
          <div class="row mb-3">
            <!-- Username -->
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
                required
                type="text"
                class="form-control"
              />
            </div>

            <!-- Password -->
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
                required
                minlength="4"
                maxlength="10"
                type="password"
                class="form-control"
              />
            </div>
          </div>

          <!-- Australian Resident and Gender -->
          <div class="row mb-3">
            <!-- Australian Resident -->
            <div class="col-md-6 col-sm-6">
              <div class="form-check resident-field">
                <input
                  id="isAustralian"
                  v-model="formData.isAustralian"
                  type="checkbox"
                  class="form-check-input"
                />

                <label
                  for="isAustralian"
                  class="form-check-label"
                >
                  Australian Resident?
                </label>
              </div>
            </div>

            <!-- Gender -->
            <div class="col-md-6 col-sm-6">
              <label
                for="gender"
                class="form-label"
              >
                Gender
              </label>

                <select
                  class="form-select"
                  id="gender"
                  required
                  v-model="formData.gender"
                >
                <option disabled value="">Please select a gender</option>
                <option value="male">Male</option>
                <option value="female">Female</option>
                <option value="other">Other</option>
              </select>
            </div>
          </div>

          <!-- Reason for joining -->
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
              required
              minlength="10"
              maxlength="200"
              rows="3"
            ></textarea>
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

    <!-- Submitted Bootstrap Cards -->
    <div
      v-if="submittedCards.length > 0"
      class="row mt-5"
    >
      <div class="col-12">
        <div class="d-flex flex-wrap justify-content-start">
          <div
            v-for="card in submittedCards"
            :key="card.id"
            class="card user-card m-2"
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
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'

/*
 * Reactive object that stores the values entered
 * into the form.
 */
const formData = reactive({
  username: '',
  password: '',
  isAustralian: false,
  gender: '',
  reason: ''
})

/*
 * Stores all submitted user-information cards.
 */
const submittedCards = ref([])

/*
 * Provides a unique ID for each submitted card.
 */
let nextCardId = 1

/*
 * Activity 1 intentionally contains no validation.
 * Even an empty form can be submitted.
 */
const submitForm = () => {
  submittedCards.value.push({
    id: nextCardId,
    username: formData.username,
    password: formData.password,
    isAustralian: formData.isAustralian,
    gender: formData.gender,
    reason: formData.reason
  })

  nextCardId += 1
}

/*
 * Clears the current form fields.
 * Submitted cards remain on the page.
 */
const clearForm = () => {
  formData.username = ''
  formData.password = ''
  formData.isAustralian = false
  formData.gender = ''
  formData.reason = ''
}
</script>

<style scoped>
/*
 * Align the checkbox with the Gender field.
 */
.resident-field {
  margin-top: 2rem;
}

/*
 * Fixed width similar to the Bootstrap cards
 * shown in the lab guide.
 */
.user-card {
  width: 18rem;
  border: 1px solid #dee2e6;
  border-radius: 0.5rem;
  overflow: hidden;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.12);
}

.card-header {
  background-color: #3867d6;
  color: white;
  padding: 0.75rem;
}

.list-group-item {
  padding: 0.75rem;
}

/*
 * On small screens, fields change to a vertical layout.
 */
@media (max-width: 767.98px) {
  .resident-field {
    margin-top: 0;
  }

  .col-sm-6 {
    margin-bottom: 1rem;
  }
}
</style>