<template>
  <div>
    <form v-on:submit="addProduct">
      <div class="col-md-3">
        <div class="form-group">
          <label>Codigo:</label>
          <input type="text" class="form-control" v-model="product.codigo"/>
        </div>
      </div>
      <div class="col-md-3">
        <div class="form-group">
          <label>Nombre:</label>
          <input type="text" class="form-control" v-model="product.nombre"/>
        </div>
      </div>
      <div class="col-md-3">
        <div class="form-group">
          <label>Precio:</label>
          <input type="number" class="form-control" v-model="product.precio"/>
        </div>
      </div>
      <div class="col-md-3">
        <div class="form-group">
          <label>Cantidad:</label>
          <input type="text" class="form-control" v-model="product.exist"/>
        </div>
      </div>
      <div class="form-group">
        <button class="btn btn-success">Agregar Producto</button>
      </div>
    </form>
    <div class="form-group">
      <button @click="updateProduct()" class="btn btn-primary">Actualizar Producto</button>
    </div>
    <!-- <b-table striped hover :items="allProducts" :fields="fields">
    </b-table> -->
    <table class="table">
      <thead>
        <tr>
          <th scope="col">id</th>
          <th scope="col">Codigo</th>
          <th scope="col">Nombre</th>
          <th scope="col">Precio</th>
          <th scope="col">Cantidad</th>
          <th scope="col">Opciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="p of allProducts">
          <th>{{p.id}}</th>
          <th>{{p.codigo}}</th>
          <th>{{p.nombre}}</th>
          <th>{{p.precio}}</th>
          <th>{{p.exist}}</th>
          <th>
            <button @click="selectProduct(p.id)" class="btn btn-info">Editar</button>
            <button @click="deleteProduct(p.id)" class="btn btn-danger">Borrar</button>
          </th>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      allProducts: [],
      product: {},
      errors: [],
      fields: [
        "id",
        "codigo",
        "nombre",
        "precio",
        { key: "exist", label: "cantidad" }
      ]
    };
  },
  created() {
    this.getProducts();
  },
  methods: {
    getProducts() {
      axios
        .get("http://localhost:8080/api/products")
        .then(response => {
          this.allProducts = response.data;
        })
        .catch(e => {
          this.errors.push(e);
        });
    },

    addProduct() {
      axios
        .post("http://localhost:8080/api/products", this.product)
        .then(response => {})
        .catch(e => {
          this.errors.push(e);
        });
    },

    updateProduct() {
      document.location.reload(true);
      axios.put("http://localhost:8080/api/products/" + this.product.id, this.product)
        .then(response => {
          getProducts();
        })
        .catch(e => {
          this.errors.push(e);
        });
    },

    selectProduct(id) {
      axios.get("http://localhost:8080/api/products/" + id)
        .then(response => {
          this.product = response.data;
        })
        .catch(e => {
          this.errors.push(e);
        });
    },

    deleteProduct(id) {
      document.location.reload(true);
      axios.delete("http://localhost:8080/api/products/" + id)
        .then(response => {
          getProducts();
        })
        .catch(e => {
          this.errors.push(e);
        });
    }
  }
};
</script>
