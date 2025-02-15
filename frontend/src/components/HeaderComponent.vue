<template>
  <header class="navbar navbar-expand-md d-flex d-md-none d-print-none ">
    <div class="container-xl">
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbar-menu"
        aria-controls="navbar-menu" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
    </div>
  </header>
  <header class="navbar-expand-md">
    <div class="collapse navbar-collapse" id="navbar-menu">
      <div class="navbar">
        <div class="container-xl">
          <div class="row flex-fill align-items-center">
            <div class="col">
              <ul class="navbar-nav">

                <li 
                  :class="{ 'nav-item': true, active: $route.path === menu.link }" 
                  v-for="(menu, index) in headerMenu" 
                  :key="index"
                > 
                  <router-link class="nav-link" :to="menu.link">
                    <span v-if="menu.icon" class="nav-link-icon d-md-none d-lg-inline-block">
                      <component :is="menu.icon" class="icon" stroke="2" />
                    </span>
                    <span class="nav-link-title">
                      {{ menu.name }}
                    </span>
                  </router-link>
                </li>
                <hr class="d-block d-md-none my-2">
                <li class="nav-item ms-auto d-none d-md-block">
                  <div class="navbar-nav flex-row order-md-last">
                    <div class="d-md-flex">
                      <a href="javascript:void(0)" @click="$theme.toggle" class="nav-link px-0 hide-theme-dark" data-bs-toggle="tooltip"
                        data-bs-placement="bottom" aria-label="Qorong'u rejimini yoqish"
                        data-bs-original-title="Qorong'u rejimini yoqish">
                        <IconMoon class="icon" stroke="2" />
                      </a>
                      <a href="javascript:void(0)" @click="$theme.toggle" class="nav-link px-0 hide-theme-light" data-bs-toggle="tooltip"
                        data-bs-placement="bottom" aria-label="Yoriq rejimini yoqish"
                        data-bs-original-title="Yoriq rejimini yoqish">
                        <IconSun class="icon" stroke="2" />
                      </a>
                    </div>
                    <div class="nav-item dropdown">
                      <a href="javascript:void(0)" class="nav-link d-flex lh-1 text-reset p-0" data-bs-toggle="dropdown"
                        aria-label="Open user menu">
                        <span class="avatar avatar-sm">
                          <IconUserFilled class="icon" stroke="2" />
                        </span>
                        <div class="d-xl-block ps-2">
                          <div>{{ full_name }}</div>
                        </div>
                      </a>
                      <div class="dropdown-menu dropdown-menu-end dropdown-menu-arrow">
                        <!-- <a href="./profile.html" class="dropdown-item">Profile</a> -->
                        <router-link class="dropdown-item" @click.prevent="handleLogout" to="">
                          <IconLogout class="icon icon-inline me-1" stroke="2" />
                          Chiqish
                        </router-link>
                      </div>
                    </div>
                  </div>
                </li>
                <li class="nav-item d-block d-md-none">
                  <div class="nav-link d-md-flex">
                    <a href="javascript:void(0)" @click="$theme.toggle" style="min-width: 0rem;" class="nav-link px-0 hide-theme-dark"
                      data-bs-toggle="tooltip" data-bs-placement="bottom">
                      <IconMoon class="icon" stroke="2" />
                      <span class="nav-link-title ps-2">Qorong'u rejimini yoqish</span>
                    </a>
                    <a href="javascript:void(0)" @click="$theme.toggle" style="min-width: 0rem;" class="nav-link px-0 hide-theme-light"
                      data-bs-toggle="tooltip" data-bs-placement="bottom">
                      <IconSun class="icon" stroke="2" />
                      <span class="nav-link-title ps-2">Yoriq rejimini yoqish</span>
                    </a>
                  </div>
                </li>
                <li class="nav-item dropdown d-block d-md-none">
                  <div class="nav-link dropdown-toggle d-flex lh-1 text-reset" data-bs-toggle="dropdown"
                    data-bs-auto-close="outside" role="button" aria-expanded="false">
                    <span class="avatar avatar-sm">
                      <IconUserFilled class="icon" stroke="2" />
                    </span>
                    <div class="d-xl-block ps-2">
                      <div>{{ full_name }}</div>
                    </div>
                  </div>
                  <div class="dropdown-menu">
                    <!-- <a href="./profile.html" class="dropdown-item">Profile</a> -->
                    <router-link class="dropdown-item" @click.prevent="handleLogout" to="">
                      <IconLogout class="icon icon-inline me-1" stroke="2" />
                      Chiqish
                    </router-link>
                  </div>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  </header>
</template>

<script>
import { IconLifebuoy, IconSun, IconMoon, IconUserFilled, IconLogout, IconHome } from '@tabler/icons-vue';
import { logout } from '@/api/auth';
import { store } from '@/store';

export default {
  name: 'HeaderComponent',
  data() {
    return {
      full_name: store.user.name,
      headerMenu: [
        {
          name: 'Bosh sahifa',
          icon: 'IconHome',
          link: '/'
        },
        {
          name: 'Gigrogeologik',
          link: '/geo'
        },
        {
          name: 'Gidromeliorativ',
          link: '/melio'
        },
        // {
        //   name: 'Gidrometeorologik',
        //   link: '/meteo'
        // },
        {
          name: 'Litologiya',
          link: '/lithology'
        }
      ]
    }
  },
  components: {
    IconLifebuoy, IconSun, IconMoon, IconUserFilled, IconLogout, IconHome
  },
  methods: {
    async handleLogout() {
      try {
        await logout();
        this.$router.push("/login");
      } catch (error) {
        console.error("Error during logout:", error);
      }
    },
  },
}
</script>