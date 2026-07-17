import { ref } from 'vue'

const storedAuthentication =
    sessionStorage.getItem('isAuthenticated')

export const isAuthenticated = ref(
    storedAuthentication === 'true'
)

const validUsername = 'libraryUser'
const validPassword = 'Library123!'

export const login = (username, password) => {
    const credentialsAreValid =
        username === validUsername &&
        password === validPassword

    if (!credentialsAreValid) {
        return false
    }

    isAuthenticated.value = true

    sessionStorage.setItem(
        'isAuthenticated',
        'true'
    )

    return true
}

export const logout = () => {
    isAuthenticated.value = false

    sessionStorage.removeItem(
        'isAuthenticated'
    )
}