SELECT "trainInfo_train"."train_name",
    (
        SELECT U0."arrival_time"
        FROM "trainInfo_stop" U0
        WHERE (
                U0."station_name" = Station 1
                AND U0."train_id" = ("trainInfo_train"."train_id")
            )
        LIMIT 1
    ) AS "source_arrival_time",
    (
        SELECT U0."arrival_time"
        FROM "trainInfo_stop" U0
        WHERE (
                U0."station_name" = Station 3
                AND U0."train_id" = ("trainInfo_train"."train_id")
            )
        LIMIT 1
    ) AS "destination_arrival_time"
FROM "trainInfo_train"
    INNER JOIN "trainInfo_stop" ON (
        "trainInfo_train"."train_id" = "trainInfo_stop"."train_id"
    )
    INNER JOIN "trainInfo_stop" T3 ON ("trainInfo_train"."train_id" = T3."train_id")
WHERE (
        "trainInfo_stop"."stop_id" IN (
            SELECT U0."stop_id"
            FROM "trainInfo_stop" U0
            WHERE U0."station_name" = Station 1
        )
        AND T3."stop_id" IN (
            SELECT U0."stop_id"
            FROM "trainInfo_stop" U0
            WHERE U0."station_name" = Station 3
        )
        AND (
            SELECT U0."arrival_time"
            FROM "trainInfo_stop" U0
            WHERE (
                    U0."station_name" = Station 1
                    AND U0."train_id" = ("trainInfo_train"."train_id")
                )
            LIMIT 1
        ) < (
            SELECT U0."arrival_time"
            FROM "trainInfo_stop" U0
            WHERE (
                    U0."station_name" = Station 3
                    AND U0."train_id" = ("trainInfo_train"."train_id")
                )
            LIMIT 1
        )
    )