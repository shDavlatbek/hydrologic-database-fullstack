<template>
  <div class="d-flex flex-column" style="height: 100vh;">
    <div class="page page-center">
      <div 
        :class="[
          'container', 'container-tight', 
          'py-4', 
          {'pe-none': submitLoading},
          {'blur1': submitLoading}
        ]"
      >
        <div class="text-center mb-4">
          <a href="javascript:void(0)" class="navbar-brand navbar-brand-autodark w100-h100">
            <IconLogin stroke="2" class="w-100 h-100" />
          </a>
        </div>
        <div class="card card-md">
          <div :class="{ progress: true, invisible: !submitLoading }">
            <div class="progress-bar progress-bar-indeterminate bg-primary"></div>
          </div>
          <div class="card-body">
            <h2 class="h2 text-center mb-4">Tizimga kirish</h2>
            <form @submit.prevent="handleLogin">
              <div class="mb-3">
                <label :class="['form-label', {'text-danger': isInvalid}]">
                  Elektron manzil
                </label>
                <input 
                  type="email" 
                  v-model="email" 
                  :class="{
                    'form-control': true, 
                    'required': true, 
                    'is-invalid': isInvalid,
                  }" 
                  @input="isInvalid = false"
                  placeholder="email@example.com" 
                  required
                />
                
              </div>
              <div class="mb-2">
                <label :class="['form-label', {'text-danger': isInvalid}]">
                  Parol
                </label>
                <div class="row g-2">
                  <div class="col">
                    <input 
                      :type="showPassword ? 'text' : 'password'" 
                      :class="{
                        'form-control': true, 
                        'required': true, 
                        'is-invalid': isInvalid,
                      }" 
                      @input="isInvalid = false"
                      v-model="password" 
                      required
                    />
                    <div v-if="isInvalid" class="invalid-feedback">{{ errorMessage }}</div>
                  </div>
                  <div class="col-auto">
                    <a 
                      href="javascript:void(0)" 
                      @click="showPassword = !showPassword" 
                      :class="['btn', 'btn-icon', {redBorder: isInvalid}]"
                      aria-label="Button"
                    >
                      <IconEye v-if="!showPassword" class="icon" stroke="2" />
                      <IconEyeOff v-else class="icon" stroke="2" />
                    </a>
                  </div>
                </div>
              </div>
              
              <div class="form-footer">
                <button type="submit" class="input-icon btn btn-primary w-100">
                  <span>Kirish</span>
                </button>
                
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { login, getMe } from "../api/auth";
import { IconLogin, IconEye, IconEyeOff } from '@tabler/icons-vue';

export default {
  data() {
    return {
      email: "",
      password: "",
      showPassword: false,
      submitLoading: false,
      isInvalid: false,
      errorMessage: null
    };
  },
  methods: {
    async handleLogin() {
      this.submitLoading = true
      try {
        await login(this.email, this.password);
        this.$router.replace("/");
      } catch (error) {
        this.isInvalid = true
        this.submitLoading = false
        this.errorMessage = error.response && error.response.status === 400
          ? "Elektron manzil yoki parol notug'ri"
          : "Server bilan bog'lanishda xatolik yuzaga keldi";
      }
    },
  },
  async created() {
    try {
      await getMe();
      this.$router.replace("/");
    } catch (error) {
      console.log(error);
    }
  },
  components: { IconLogin, IconEye, IconEyeOff }
};
</script>