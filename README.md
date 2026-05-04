# boundary-value-problem

## Схема
### Входные данные:
$k(x) > 0$ - коэффициент теплопроводности в сечении с координатой $x$  
$q(x) \ge 0$ - коэффициент теплообмена с окружающей средой через  боковую поверхность в сечении с координатой $x$  
$f(x)$ - плотность источников (стоков тепла) в сечении с координатой $x$  
### Вводимые аргументы:
$$\large \varphi_i = \frac{1}{h} \int_{x_{i-\frac{1}{2}}}^{x_{i+\frac{1}{2}}} f(x) \, dx, \quad i = 1,n-1$$
$$\large d_i = \frac{1}{h} \int_{x_{i-\frac{1}{2}}}^{x_{i+\frac{1}{2}}} q(x) \, dx, \quad i = 1,n-1$$
$$\large a_i = [\frac{1}{h} \int_{x_{i-1}}^{x_{i}} \frac{dx}{k(x)} \, ]^{-1}, \quad i = 1,n-1$$
### Схема:
$$ \large
\begin{cases}
V_o = \mu_0\\
a_{i+1}\frac{V_{i+1} - V_{i}}{h^2} - a_i \frac{V_i - V_{i-1}}{h^2} - d_i V_i = -\varphi_i, \quad i = 1,n-1\\
V_n = \mu_n
\end{cases}
$$

---
## Инструкция по сборке

*Используемая версия Python:* **3.14**.

На Linux необходимо установить `dev` версию python:
```Shell
sudo apt install python3.14-dev
```

#### 1. Создать виртуальное окружение
```Shell
py -m venv .venv
```

*Команда `py` может не работать на Linux.*
#### 2. Активировать виртуальное окружение
```Shell
./.venv/Scripts/activate
```
#### 3. Установить библиотеки
```Shell
pip install -r "requirements.txt"
```
#### 4. Папка для сборки
```bash
mkdir build
cd build
```
#### 5. Генерация файлов сборки
```bash
cmake .. 
```
#### 6. Компиляция программы
```bash
cmake --build .
```

--- 
## Запуск

Для запуска введите следующую команду:
```Shell
streamlit run .\python\main.py
```

---
### Другое
#### Intellisense для Vs Code
Добавьте деректорию `./python` как дополнительный путь в `python.analysis.extraPaths`
```json
"python.analysis.extraPaths": ["${workspaceFolder}/python"]
```