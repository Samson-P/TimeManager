CREATE TABLE dt_control(  
    id int NOT NULL PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    title TEXT NOT NULL,
    description TEXT,
    dt_start TEXT NOT NULL,
    interval TEXT NOT NULL,
    hash TEXT NOT NULL,

    create_time DATE
);
COMMENT ON TABLE dt_control IS 'Таблица кругов TMv5';
COMMENT ON COLUMN dt_control.title IS 'Краткое описание (название) текущего рода деятельности';
COMMENT ON COLUMN dt_control.dt_start IS 'Дата время начала круга %d-%m-%Y %H:%M:%S';
COMMENT ON COLUMN dt_control.hash IS 'При нажатии кнопки старт генерится хэш для prometheus';