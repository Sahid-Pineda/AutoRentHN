def facturacion_venta(request):
    context = {
        'factura': {
            'cliente': {
                'id': None,
                'nombre_completo': '',
                'telefono': '',
                'correo': '',
                'rtn': 'N/A'
            },
            'vehiculo': {
                'id': None,
                'marca': '',
                'modelo': '',
                'anio': '',
                'vin': '',
                'precio': 0.0
            },
            'empleado': {
                'nombre_completo': ''
            },
            'contrato': {
                'id': None,
                'tipo': '',
                'fecha': None,
                'monto': 0.0
            },
            'pagos': [],
            'calculos': {
                'subtotal': 0.0,
                'impuesto': 0.0,
                'total': 0.0,
                'cantidad': 1
            },
            'cai': '',
            'numero_documento_fiscal': ''
        }
    }

    contrato_id = request.session.get('id_contrato')
    print(f"DATOS CONTRATO ID==: {contrato_id}")
    if not contrato_id:
        logger.warning("No se encontró id_contrato en la sesión")
        messages.error(request, "No se encontró el contrato en la sesión.")
        return redirect(reverse('seleccionar_contratos'))

    try:
        contrato = traer_contrato_venta_id(contrato_id)
        print(f"DATOS CONTRATO¨¨: {contrato}")
        if not contrato:
            print("aaaa",logger.error(f"Contrato con ID {contrato_id} no encontrado"))
            messages.error(request, "El contrato no fue encontrado.")
            return redirect(reverse('seleccionar_contratos'))

        cliente = traer_cliente_id(contrato.get('cliente_id'))
        vehiculo = traer_vehiculo_id(contrato.get('vehiculo_id'))
        empleado = traer_empleado(request.session.get('user_id'))
        metodos_pago = obtener_metodos_pago()
        rangos_facturacion = obtener_rangos_facturacion_disponibles()  # Factura de venta
        
        if not rangos_facturacion:
            logger.error("No se encontraron rangos autorizados válidos para facturación de venta")
            messages.error(request, "No se encontró un rango autorizado válido para la facturación.")
            return redirect(reverse('seleccionar_contratos'))

        print(f"CLIENTE: {cliente}\n\nVEHICULO: {vehiculo}\n\n EMPLEADO{empleado}\n\nMETODO:{metodos_pago}\n\nRANGO;{rangos_facturacion}")
        if not all([cliente, vehiculo, empleado, metodos_pago, rangos_facturacion]):
            logger.error("Faltan datos relacionados al contrato")
            messages.error(request, "Error al obtener datos relacionados al contrato.")
            return redirect(reverse('seleccionar_contratos'))

        # Seleccionar rango de facturación automáticamente
        fecha_actual = datetime.now()
        rango_seleccionado = None
        for rango in rangos_facturacion:
            if (rango.get('TipoDocumento_id') == 1 and
                rango.get('FechaInicio') <= fecha_actual <= rango.get('FechaFin')):
                siguiente_numero = obtener_siguiente_numero_factura(rango)
                if siguiente_numero:
                    rango_seleccionado = rango
                    break

        if not rango_seleccionado:
            logger.error("No se encontró un rango de facturación válido")
            messages.error(request, "No hay rangos de facturación disponibles para la fecha actual.")
            return redirect(reverse('seleccionar_contratos'))

        cai = rango_seleccionado.get('CAI')
        numero_documento_fiscal = siguiente_numero

        subtotal = float(contrato.get('monto', 0))
        impuesto_total = round(subtotal * 0.15, 2) if not cliente.get('tipoexoneracion_id') else 0.0
        total = subtotal + impuesto_total

        context['factura'].update({
            'cliente': {
                'id': cliente.get('cliente_id'),
                'nombre_completo': f"{cliente.get('nombre', '')} {cliente.get('segundonombre', '')} {cliente.get('apellido', '')} {cliente.get('segundoapellido', '')}".strip(),
                'telefono': cliente.get('telefono', 'N/A'),
                'correo': cliente.get('correo', 'N/A'),
                'rtn': cliente.get('rtn', 'N/A')
            },
            'vehiculo': {
                'id': vehiculo.get('id_vehiculo'),
                'marca': vehiculo.get('marca_nombre', ''),
                'modelo': vehiculo.get('modelo_nombre', ''),
                'anio': vehiculo.get('anio', ''),
                'vin': vehiculo.get('vin', ''),
                'precio': float(vehiculo.get('precio_de_venta', 0))
            },
            'empleado': {
                'nombre_completo': f"{empleado.get('nombre', '')} {empleado.get('apellido', '')}".strip()
            },
            'contrato': {
                'id': contrato.get('id_contrato'),
                'tipo': contrato.get('tipocontrato', ''),
                'fecha': contrato.get('fecha'),
                'monto': subtotal
            },
            'pagos': metodos_pago,
            'calculos': {
                'subtotal': subtotal,
                'impuesto': impuesto_total,
                'total': total,
                'cantidad': 1
            },
            'cai': cai,
            'numero_documento_fiscal': numero_documento_fiscal
        })

        if request.method == "POST":
            try:
                cantidad = int(request.POST.get('cantidad', 1))
                precio_unitario = float(request.POST.get('precio_unitario', subtotal))
                subtotal = cantidad * precio_unitario
                impuesto = round(subtotal * 0.15, 2) if not cliente.get('tipoexoneracion_id') else 0.0
                total_form = subtotal + impuesto

                data = {
                    'contrato_id': contrato_id,
                    'cliente': cliente,
                    'vehiculo': vehiculo,
                    'empleado': empleado,
                    'cai': cai,
                    'rango_autorizado_id': rango_seleccionado.get('id_RangoAutorizado'),
                    'numero_documento_fiscal': numero_documento_fiscal,
                    'es_exonerado': bool(cliente.get('tipoexoneracion_id')),
                    'estado': 'Emitido',
                    'descripcion': request.POST.get('descripcion'),
                    'cantidad': cantidad,
                    'precio_unitario': precio_unitario,
                    'subtotal': subtotal,
                    'impuesto_total': impuesto,
                    'total_linea': subtotal,
                    'total': total_form,
                    'pagos': []
                }
                print(f"INFO DATA: {data}")

                metodo_pago_ids = request.POST.getlist('metodo_pago_id')
                montos = request.POST.getlist('monto')
                referencias = request.POST.getlist('referencia')

                for metodo_id, monto, referencia in zip(metodo_pago_ids, montos, referencias):
                    if monto and float(monto) > 0:
                        data['pagos'].append({
                            'metodo_pago_id': int(metodo_id),
                            'monto': float(monto),
                            'referencia': referencia or ''
                        })

                total_pagos = sum(pago['monto'] for pago in data['pagos'])
                if abs(total_pagos - total_form) > 0.01:
                    logger.warning(f"La suma de los pagos ({total_pagos}) no coincide con el total ({total_form})")
                    messages.error(request, "La suma de los pagos no coincide con el total de la factura.")
                    context['factura']['calculos'].update({
                        'subtotal': subtotal,
                        'impuesto_total': impuesto,
                        'total': total_form,
                        'cantidad': cantidad
                    })
                    context['factura']['descripcion'] = data['descripcion']
                    return render(request, 'facturacion/facturacion_venta.html', context)

                valor = registrar_factura_y_pago(data)
                if valor == 1:
                    messages.success(request, "Factura generada exitosamente.")
                    return redirect('empleado_view')
                else:
                    logger.error("Error al registrar la factura")
                    messages.error(request, "Error al registrar la factura.")
                    return render(request, 'facturacion/facturacion_venta.html', context)

            except ValueError as ve:
                logger.error(f"Error en los datos del formulario: {str(ve)}")
                messages.error(request, "Los datos ingresados no son válidos. Verifique los valores numéricos.")
                return render(request, 'facturacion/facturacion_venta.html', context)

            except Exception as e:
                logger.error(f"Error al procesar factura: {str(e)}", exc_info=True)
                messages.error(request, f"Error al procesar la factura: {str(e)}")
                return render(request, 'facturacion/facturacion_venta.html', context)

        logger.debug(f"Datos preparados para el template: {context}")
        return render(request, 'facturacion/facturacion_venta.html', context)

    except Exception as e:
        logger.error(f"Error al preparar daparatos para facturación: {str(e)}", exc_info=True)
        messages.error(request, "Error al preparar datos  facturación.")
        return redirect(reverse('seleccionar_contratos'))

def facturacion_alquiler(request):
    context = {
        'factura': {
            'cliente': {
                'id': None,
                'nombre_completo': '',
                'telefono': '',
                'correo': '',
                'rtn': 'N/A'
            },
            'vehiculo': {
                'id': None,
                'marca': '',
                'modelo': '',
                'anio': '',
                'vin': '',
                'precio': 0.0
            },
            'empleado': {
                'nombre_completo': ''
            },
            'contrato': {
                'id': None,
                'tipo': '',
                'fecha': None,
                'monto': 0.0,
                'fecha_inicio': None,
                'fecha_fin': None
            },
            'pagos': [],
            'calculos': {
                'subtotal': 0.0,
                'impuesto': 0.0,
                'total': 0.0,
                'cantidad': 1
            },
            'cai': '',
            'numero_documento_fiscal': ''
        }
    }

    contrato_id = request.session.get('id_contrato')
    if not contrato_id:
        logger.warning("No se encontró id_contrato en la sesión")
        messages.error(request, "No se encontró el contrato en la sesión.")
        return redirect(reverse('seleccionar_contratos'))

    try:
        contrato = traer_contrato_alquiler_id(contrato_id)
        if not contrato:
            logger.error(f"Contrato con ID {contrato_id} no encontrado o no es de alquiler")
            messages.error(request, "El contrato no fue encontrado o no es de alquiler.")
            return redirect(reverse('seleccionar_contratos'))

        cliente = traer_cliente_id(contrato.get('cliente_id'))
        vehiculo = traer_vehiculo_id(contrato.get('vehiculo_id'))
        empleado = traer_empleado(request.session.get('user_id'))
        metodos_pago = obtener_metodos_pago()
        rangos_facturacion = obtener_rangos_facturacion_disponibles(tipo_documento_id=1)

        if not all([cliente, vehiculo, empleado, metodos_pago, rangos_facturacion]):
            logger.error("Faltan datos relacionados al contrato")
            messages.error(request, "Error al obtener datos relacionados al contrato.")
            return redirect(reverse('seleccionar_contratos'))

        fecha_actual = datetime.now()
        rango_seleccionado = None
        for rango in rangos_facturacion:
            if (rango.get('TipoDocumento_id') == 1 and
                rango.get('FechaInicio') <= fecha_actual <= rango.get('FechaFin')):
                siguiente_numero = obtener_siguiente_numero_factura(rango)
                if siguiente_numero:
                    rango_seleccionado = rango
                    break

        if not rango_seleccionado:
            logger.error("No se encontró un rango de facturación válido para alquiler")
            messages.error(request, "No hay rangos de facturación disponibles para la fecha actual.")
            return redirect(reverse('seleccionar_contratos'))

        cai = rango_seleccionado.get('CAI')
        numero_documento_fiscal = siguiente_numero

        # Calcular el monto basado en el precio de alquiler y la duración
        precio_diario = float(vehiculo.get('precio_de_alquiler', 0))
        fecha_inicio = contrato.get('fechainicioalquiler')
        fecha_fin = contrato.get('fechafinalquiler')
        if fecha_inicio and fecha_fin:
            dias_alquiler = (fecha_fin - fecha_inicio).days + 1
            subtotal = precio_diario * dias_alquiler
        else:
            subtotal = precio_diario  # a un día si las fechas no están disponibles
        impuesto_total = round(subtotal * 0.18, 2) if not cliente.get('tipoexoneracion_id') else 0.0
        total = subtotal + impuesto_total

        context['factura'].update({
            'cliente': {
                'id': cliente.get('cliente_id'),
                'nombre_completo': f"{cliente.get('nombre', '')} {cliente.get('segundonombre', '')} {cliente.get('apellido', '')} {cliente.get('segundoapellido', '')}".strip(),
                'telefono': cliente.get('telefono', 'N/A'),
                'correo': cliente.get('correo', 'N/A'),
                'rtn': cliente.get('rtn', 'N/A')
            },
            'vehiculo': {
                'id': vehiculo.get('id_vehiculo'),
                'marca': vehiculo.get('marca_nombre', ''),
                'modelo': vehiculo.get('modelo_nombre', ''),
                'anio': vehiculo.get('anio', ''),
                'vin': vehiculo.get('vin', ''),
                'precio': float(vehiculo.get('precio_de_alquiler', 0))
            },
            'empleado': {
                'nombre_completo': f"{empleado.get('nombre', '')} {empleado.get('apellido', '')}".strip()
            },
            'contrato': {
                'id': contrato.get('id_contrato'),
                'tipo': contrato.get('tipocontrato', ''),
                'fecha': contrato.get('fecha'),
                'monto': subtotal,
                'fecha_inicio': fecha_inicio,
                'fecha_fin': fecha_fin
            },
            'pagos': metodos_pago,
            'calculos': {
                'subtotal': subtotal,
                'impuesto': impuesto_total,
                'total': total,
                'cantidad': dias_alquiler if fecha_inicio and fecha_fin else 1
            },
            'cai': cai,
            'numero_documento_fiscal': numero_documento_fiscal
        })

        if request.method == "POST":
            try:
                cantidad = int(request.POST.get('cantidad', context['factura']['calculos']['cantidad']))
                precio_unitario = float(request.POST.get('precio_unitario', precio_diario))
                subtotal = cantidad * precio_unitario
                impuesto = round(subtotal * 0.18, 2) if not cliente.get('tipoexoneracion_id') else 0.0
                total_form = subtotal + impuesto

                data = {
                    'contrato_id': contrato_id,
                    'cliente': cliente,
                    'vehiculo': vehiculo,
                    'empleado': empleado,
                    'cai': cai,
                    'rango_autorizado_id': rango_seleccionado.get('id_rangoautorizado'),
                    'numero_documento_fiscal': numero_documento_fiscal,
                    'es_exonerado': bool(cliente.get('tipoexoneracion_id')),
                    'estado': 'Emitido',
                    'descripcion': request.POST.get('descripcion', f"Alquiler de vehículo {vehiculo.get('marca_nombre')} {vehiculo.get('modelo_nombre')}"),
                    'cantidad': cantidad,
                    'precio_unitario': precio_unitario,
                    'subtotal': subtotal,
                    'impuesto': impuesto,
                    'total_linea': subtotal,
                    'total': total_form,
                    'pagos': []
                }

                metodo_pago_ids = request.POST.getlist('metodo_pago_id')
                montos = request.POST.getlist('monto')
                referencias = request.POST.getlist('referencia')

                for metodo_id, monto, referencia in zip(metodo_pago_ids, montos, referencias):
                    if monto and float(monto) > 0:
                        data['pagos'].append({
                            'metodo_pago_id': int(metodo_id),
                            'monto': float(monto),
                            'referencia': referencia or ''
                        })

                total_pagos = sum(pago['monto'] for pago in data['pagos'])
                if abs(total_pagos - total_form) > 0.01:
                    logger.warning(f"La suma de los pagos ({total_pagos}) no coincide con el total ({total_form})")
                    messages.error(request, "La suma de los pagos no coincide con el total de la factura.")
                    context['factura']['calculos'].update({
                        'subtotal': subtotal,
                        'impuesto': impuesto,
                        'total': total_form,
                        'cantidad': cantidad
                    })
                    context['factura']['descripcion'] = data['descripcion']
                    return render(request, 'facturacion/facturacion_alquiler.html', context)

                valor = registrar_factura_y_pago(data)
                if valor:
                    actualizar_estado_contrato(contrato_id)
                    messages.success(request, "Factura generada exitosamente.")
                    return redirect('empleado_view')
                else:
                    logger.error("Error al registrar la factura")
                    messages.error(request, "Error al registrar la factura.")
                    return render(request, 'facturacion/facturacion_alquiler.html', context)

            except ValueError as ve:
                logger.error(f"Error en los datos del formulario: {str(ve)}")
                messages.error(request, "Los datos ingresados no son válidos. Verifique los valores numéricos.")
                return render(request, 'facturacion/facturacion_alquiler.html', context)

            except Exception as e:
                logger.error(f"Error al procesar factura: {str(e)}", exc_info=True)
                messages.error(request, f"Error al procesar la factura: {str(e)}")
                return render(request, 'facturacion/facturacion_alquiler.html', context)

        logger.debug(f"Datos preparados para el template: {context}")
        return render(request, 'facturacion/facturacion_alquiler.html', context)

    except Exception as e:
        logger.error(f"Error al preparar datos para facturación: {str(e)}", exc_info=True)
        messages.error(request, "Error al preparar datos para facturación.")
        return redirect(reverse('seleccionar_contratos'))