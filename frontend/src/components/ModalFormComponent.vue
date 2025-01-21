<template>
  <form @submit.prevent="handleSubmit">
  <div class="modal modal-blur fade" :id="modalId" tabindex="-1" role="dialog" data-bs-backdrop="static">
    <div class="modal-dialog modal-xl modal-dialog-centered" :class="{ 'modal-dialog-scrollable': scrollable }" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">{{ modalTitle }}</h5>
          <button type="button" class="btn-close" id="close-modal-form" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <slot name="modal-body"></slot>
          <div class="modal-footer">
            <button class="btn btn-link link-secondary" data-bs-dismiss="modal">
              Bekor qilish
            </button>
            <span class="ms-auto"></span>
            <slot name="modal-footer-buttons"></slot>
            <input type="reset" class="btn" value="Tozalash" />
            <button type="submit" class="btn btn-primary">
              <IconPlus class="icon" stroke="2" />
              Qo'shish
            </button>
          </div>
        
          
      </div>
    </div>
  </div>
  </form>
</template>

<script>
import { IconPlus } from '@tabler/icons-vue';
import { Modal } from 'bootstrap';


export default {
  name: 'ModalForm',
  data() {
    return {
      modalInstance: null
    };
  },
  mounted() {
    this.modalInstance = Modal.getOrCreateInstance(`#${this.modalId}`)
  },
  props: {
    modalId: {
      type: String,
      required: true
    },
    modalTitle: {
      type: String,
      required: true
    },
    modalFormConfirm: {
      type: Function,
      required: true
    },
    scrollable: {
      type: Boolean,
      default: false
    }
  },
  components: {
    IconPlus
  },
  methods: {
    async handleSubmit(event) {
      const form = event.target;
      if (form.checkValidity()) {
        await this.modalFormConfirm();
        form.reset();
      } else {
        form.reportValidity();
      }
    },
    openModal() {
      this.modalInstance.show();
    },
    closeModal(){
      document.getElementById('close-modal-form').click();
    },
    resetForm() {
      const form = document.querySelector(`#${this.modalId} form`);
      form.reset();
    }
  }
}

</script>