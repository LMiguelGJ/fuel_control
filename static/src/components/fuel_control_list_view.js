/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListController } from "@web/views/list/list_controller";

const { onMounted } = owl;

class AttendanceListViewController extends ListController {
    setup() {
        super.setup();
        console.log("Attendance list inherited!");

        // Llama al método fetchTotal cuando el componente se monte
        onMounted(() => {
            this.controlPanel()
            this.loadSavedDates()
            this.setupClearFilterListener()
            this.setupDateFieldListeners()
            this.fetchTotal();
        });
    }

    async fetchTotal() {
        try {
            // Realiza una llamada RPC para obtener el total del modelo `fuel.control`
            const response = await this.rpc(
                "/web/dataset/call_kw/fuel.control/search_read",
                {
                    model: "fuel.control",
                    method: "search_read",
                    args: [],
                    kwargs: {
                        domain: [],
                        fields: ["total"],
                        order: "create_date desc",
                        limit: 1,
                    },
                }
            );

            // Verifica si se obtuvo un registro y actualiza el contenido del elemento HTML
            if (response && response.length > 0) {
                const totalValue = response[0].total;

                // Busca el elemento por clase y asigna el valor
                const totalElement = document.querySelector(
                    ".form-control.form-control-lg.h2.fs-2.text-center"
                );
                if (totalElement) {
                    totalElement.textContent = totalValue;
                    console.log("Total actualizado:", totalValue);
                } else {
                    console.warn("No se encontró el elemento para mostrar el total");
                }
            } else {
                console.log("No se encontraron registros en fuel.control");
            }
        } catch (error) {
            console.error("Error fetching data:", error);
        }
    }
    controlPanel() {
        const controlPanel = document.querySelector(".o_control_panel")
        if (controlPanel) {
            const newDiv = document.createElement('div')
            newDiv.className = 'o_onboarding_panel'
            newDiv.style.cssText = 'display: flex; align-items: center; justify-content: space-between; width: 96%; margin: 0.5% 2%;'
            newDiv.innerHTML = `
            <div class="o_onboarding_panel_step d-flex align-items-center">
                <form class="d-flex align-items-center" id="dateFilterForm">
                    <!-- Fecha desde -->
                    <label for="date_from" class="me-2">Desde:</label>
                    <input type="text" placeholder="Ingrese la fecha" id="date_from" name="date_from" class="form-control me-4 border rounded p-2" />
    
                    <!-- Fecha hasta -->
                    <label for="date_to" class="me-2">Hasta:</label>
                    <input type="text" placeholder="Ingrese la fecha" id="date_to" name="date_to" class="form-control me-4 border rounded p-2" />
                    
                    <!-- Botón Aplicar -->
                    <button type="submit" class="btn btn-primary">
                        Aplicar
                    </button>

                    <!-- Botón Borrar Filtro -->
                    <a class="btn btn-outline-dark ms-3 text-nowrap">
                        BORRAR FILTRO
                    </a>
                </form>
            </div>
            <div class="d-flex justify-content-center flex-row align-items-center gap-2">
                <h1 class="h1 fs-1">Total:</h1>
                <span t-esc="total" class="form-control form-control-lg h2 fs-2 text-center fw-bold"></span>
                <h1 class="h1 fs-1">GL</h1>
            </div>
            `
            controlPanel.appendChild(newDiv)

            // Agregar listener para el formulario
            const dateFilterForm = document.getElementById('dateFilterForm')
            dateFilterForm.addEventListener('submit', (event) => {
                event.preventDefault()
                this.applyDateFilter()
            })
        }
    }

    setupClearFilterListener() {
        const clearFilterButton = document.querySelector('.o_onboarding_panel a.btn-outline-dark')
        if (clearFilterButton) {
            clearFilterButton.addEventListener('click', (event) => {
                event.preventDefault()
                this.clearFilters()
            })
        } else {
            console.warn('No se encontró el botón de borrar filtro')
        }
    }

    clearFilters() {
        // Limpiar fechas en localStorage
        localStorage.removeItem('attendanceDateFrom')
        localStorage.removeItem('attendanceDateTo')

        // Limpiar todos los campos de filtro
        document.getElementById('date_from').value = ''
        document.getElementById('date_to').value = ''
        
        // Volver a la vista original
        this.env.services.action.doAction({
            type: 'ir.actions.act_window',
            name: 'Ver Transacciones',
            res_model: 'fuel.control',
            view_mode: 'list',
            views: [[false, 'list']],
            target: 'current',
            domain: [],
        })
    }

    loadSavedDates() {
        const dateFrom = localStorage.getItem('attendanceDateFrom')
        const dateTo = localStorage.getItem('attendanceDateTo')
        
        if (dateFrom) {
            document.getElementById('date_from').value = dateFrom
        }
        if (dateTo) {
            document.getElementById('date_to').value = dateTo
        }
    }

    setupDateFieldListeners() {
        const dateFields = ['date_from', 'date_to']
        dateFields.forEach(fieldId => {
            const field = document.getElementById(fieldId)
            if (field) {
                field.addEventListener('click', function() {
                    this.type = 'date'
                    if (this.showPicker) {
                        this.showPicker()
                    }
                })
                field.addEventListener('blur', function() {
                    if (this.value === '') {
                        this.type = 'text'
                    }
                })
            } else {
                console.warn(`No se encontró el campo ${fieldId}`)
            }
        })
    }

    applyDateFilter() {
        const dateFrom = document.getElementById('date_from').value
        const dateTo = document.getElementById('date_to').value

        if (!dateFrom && !dateTo) {
            alert("Por favor, ingrese al menos una fecha (Desde o Hasta).");
            return; // Salir de la función si ambos campos están vacíos
        }

        // Aplicar el filtro a la vista
        const domain = []
        if (dateFrom) {
            domain.push(['date', '>=', dateFrom])
        }
        if (dateTo) {
            domain.push(['date', '<=', dateTo])
        }

        const filterName = `(${dateFrom} - ${dateTo})`;


        this.env.services.action.doAction({
            type: 'ir.actions.act_window',
            name: filterName,
            res_model: 'fuel.control',
            view_mode: 'list',
            views: [[false, 'list']],
            target: 'current',
            domain: domain,
        })
    }
}

const attendanceListView = {
    ...listView,
    Controller: AttendanceListViewController,
}

registry.category("views").add("fuel_control_list_view", attendanceListView)
