# Diagramas UML del Proyecto

## 1. Diagrama de Clases

El siguiente diagrama de clases representa la estructura, atributos, métodos y relaciones de las clases principales dentro del directorio `src/` (módulos `data/`, `models/` y `utils/`).

```mermaid
classDiagram
    class DataLoader {
        +Path filepath
        +DataFrame df
        +load() DataFrame
        +resumen_calidad() DataFrame
        +detectar_duplicados() int
        +descripcion_general() dict
    }

    class DataPreprocessor {
        +int random_state
        +DataFrame df_clean
        -StandardScaler edad_scaler
        +fit_transform(DataFrame df) DataFrame
        -manejar_valores_faltantes(DataFrame df) DataFrame
        -crear_variable_severidad(DataFrame df) DataFrame
        -encoding_categoricas(DataFrame df) DataFrame
        -escalar_numericas(DataFrame df) DataFrame
        +exportar(DataFrame df, str filename) void
        +split_datos(DataFrame df, str target_col, float test_size) Tuple
    }

    class ModelFactory {
        +int random_state
        +dict MODELOS_SOPORTADOS
        +create_model(str tipo, dict kwargs) Any
        +listar_modelos() list
    }

    class ModelTrainer {
        +int random_state
        +dict best_params
        +dict cv_results
        +entrenar(Any modelo, DataFrame X_train, Series y_train) Any
        +validacion_cruzada(Any modelo, DataFrame X, Series y, int cv) dict
        +busqueda_hiperparametros(Any modelo, dict param_grid, DataFrame X_train, Series y_train, int cv) Any
        +serializar_modelo(Any modelo, str nombre) void
    }

    class ModelEvaluator {
        +dict resultados
        +evaluar(Any modelo, DataFrame X_test, Series y_test) dict
        +matriz_confusion(Any modelo, DataFrame X_test, Series y_test) void
        +curva_roc(Any modelo, DataFrame X_test, Series y_test) void
        +comparar_modelos(list modelos, DataFrame X_test, Series y_test) DataFrame
        +evaluar_baseline(Series y_test) dict
        +feature_importance(Any modelo, list feature_names, int top_n) void
    }

    class ClusterAnalyzer {
        +int random_state
        +ndarray labels
        +int n_clusters
        +StandardScaler scaler_
        +PCA pca_model_
        +KMeans km_model_
        +ndarray linkage_matrix_
        +normalizar(DataFrame df, list columnas) DataFrame
        +metodo_codo(DataFrame X, range k_range) dict
        +coeficiente_silueta(DataFrame X, range k_range) dict
        +fit_kmeans(DataFrame X, int n_clusters) ndarray
        +dendrograma(DataFrame X, str metodo, list labels_texto) ndarray
        +fit_jerarquico(DataFrame X, int n_clusters, str metodo) ndarray
        +reducir_dimensionalidad(DataFrame X, str metodo, int n_componentes) DataFrame
        +visualizar_clusters(DataFrame X_reducido, ndarray labels, str titulo) void
        +perfilar_clusters(DataFrame df, ndarray labels) DataFrame
    }

    class AssociationRuleMiner {
        +DataFrame reglas
        +DataFrame itemsets_frecuentes
        +preparar_datos(DataFrame df, list columnas) DataFrame
        +ejecutar_apriori(DataFrame df_binario, float min_support) DataFrame
        +generar_reglas(str metric, float min_threshold) DataFrame
        +top_reglas(int n, str ordenar_por) DataFrame
    }

    %% Relaciones y Dependencias
    DataPreprocessor ..> DataLoader : procesa salida de carga
    ModelTrainer ..> ModelFactory : usa
    ModelEvaluator ..> ModelTrainer : evalua
    ClusterAnalyzer ..> DataPreprocessor : usa datos limpios
    AssociationRuleMiner ..> DataPreprocessor : usa datos limpios
```

## 2. Arquitectura del Sistema y Flujo de Datos

El siguiente diagrama detalla el flujo operativo de los datos, desde la ingesta del archivo crudo, pasando por el preprocesamiento, hasta los módulos de análisis paralelos.

```mermaid
flowchart TD
    subgraph Capa de Datos Crudos
        A["COVID19MEXICO_raw.csv"]
    end

    subgraph Carga y Preparacion de Datos
        B["DataLoader"] -->|"DataFrame Crudo"| C["DataPreprocessor"]
        C -->|"fit_transform()"| D["COVID19MEXICO_clean.csv"]
    end

    subgraph Analisis y Mineria de Datos
        D -->|"Comorbilidades (bool)"| E["AssociationRuleMiner"]
        D -->|"Clinicos y Demograficos"| F["ClusterAnalyzer"]
        D -->|"split_datos()"| G["X_train, y_train, X_test, y_test"]
    end

    subgraph Aprendizaje Automatico Supervisado
        H["ModelFactory"] -->|"Instancia dt / rf / xgb"| I["ModelTrainer"]
        G -->|"Particion Entrenamiento"| I
        I -->|"fit() / tune()"| J["Estimadores Entrenados"]
        J -->|"predict() / predict_proba()"| K["ModelEvaluator"]
        G -->|"Particion Prueba"| K
    end

    E -->|"Reglas de Apriori"| L["Reglas de Asociacion y Metricas de Lift"]
    F -->|"K-Means / PCA / Jerarquico"| M["Perfiles de Paciente y Clusters"]
    K -->|"Metricas / Matriz de Confusion / ROC-AUC"| N["Reportes de Evaluacion"]
```
