"""
ModelFactory — Patrón Factory Method para clasificadores.

Crea instancias de Decision Tree, Random Forest o XGBoost con una
interfaz unificada, permitiendo intercambiar algoritmos sin modificar
el código cliente.

Colaborador responsable: C (Modelo Supervisado)
"""

from typing import Any

from src.utils.constants import RANDOM_STATE


class ModelFactory:
    """Factory Method para crear clasificadores de forma intercambiable.

    Modelos soportados:
        - ``'dt'``  → DecisionTreeClassifier
        - ``'rf'``  → RandomForestClassifier
        - ``'xgb'`` → XGBClassifier

    Examples
    --------
    >>> factory = ModelFactory()
    >>> modelo_dt = factory.create_model('dt', max_depth=5)
    >>> modelo_rf = factory.create_model('rf', n_estimators=200)
    >>> modelo_xgb = factory.create_model('xgb', learning_rate=0.1)
    """

    # Registro de tipos soportados y sus parámetros por defecto
    _MODELOS_SOPORTADOS: dict[str, str] = {
        "dt": "DecisionTreeClassifier",
        "rf": "RandomForestClassifier",
        "xgb": "XGBClassifier",
    }

    def __init__(self, random_state: int = RANDOM_STATE):
        self.random_state = random_state

    def create_model(self, tipo: str, **kwargs: Any):
        """Crea y retorna una instancia del clasificador solicitado.

        Parameters
        ----------
        tipo : str
            Tipo de modelo: ``'dt'``, ``'rf'`` o ``'xgb'``.
        **kwargs
            Hiperparámetros adicionales para el constructor del modelo.

        Returns
        -------
        Clasificador de scikit-learn o XGBoost.

        Raises
        ------
        ValueError
            Si ``tipo`` no está en los modelos soportados.
        """
        # TODO: Implementar creación de modelos con parámetros por defecto
        raise NotImplementedError(f"Implementar creación de modelo '{tipo}'")

    def listar_modelos(self) -> list[str]:
        """Retorna los tipos de modelos soportados.

        Returns
        -------
        list[str]
            Lista de claves válidas para ``create_model()``.
        """
        return list(self._MODELOS_SOPORTADOS.keys())
