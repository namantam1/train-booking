SELECT "idea3_train"."id",
    "idea3_train"."name",
    "idea3_train"."seats_count",
    (
        SELECT U0."arrival_time"
        FROM "idea3_stop" U0
        WHERE (
                U0."station_name" = Station 1
                AND U0."train_id" = ("idea3_train"."id")
            )
        LIMIT 1
    ) AS "source_arrival_time",
    (
        SELECT U0."arrival_time"
        FROM "idea3_stop" U0
        WHERE (
                U0."station_name" = Station 3
                AND U0."train_id" = ("idea3_train"."id")
            )
        LIMIT 1
    ) AS "destination_arrival_time",
    (
        SELECT CASE
                WHEN U0."seats_booked" IS NULL THEN NULL
                ELSE coalesce(array_length(U0."seats_booked", 1), 0)
            END
        FROM "idea3_stop" U0
        WHERE (
                U0."arrival_time" >= (
                    SELECT U0."arrival_time"
                    FROM "idea3_stop" U0
                    WHERE (
                            U0."station_name" = Station 1
                            AND U0."train_id" = ("idea3_train"."id")
                        )
                    LIMIT 1
                )
                AND U0."arrival_time" <= (
                    SELECT U0."arrival_time"
                    FROM "idea3_stop" U0
                    WHERE (
                            U0."station_name" = Station 3
                            AND U0."train_id" = ("idea3_train"."id")
                        )
                    LIMIT 1
                )
                AND U0."train_id" = ("idea3_train"."id")
            )
        ORDER BY CASE
                WHEN U0."seats_booked" IS NULL THEN NULL
                ELSE coalesce(array_length(U0."seats_booked", 1), 0)
            END ASC
        LIMIT 1
    ) AS "seats"
FROM "idea3_train"
    INNER JOIN "idea3_stop" ON ("idea3_train"."id" = "idea3_stop"."train_id")
    INNER JOIN "idea3_stop" T3 ON ("idea3_train"."id" = T3."train_id")
WHERE (
        "idea3_stop"."id" IN (
            SELECT U0."id"
            FROM "idea3_stop" U0
            WHERE U0."station_name" = Station 1
        )
        AND T3."id" IN (
            SELECT U0."id"
            FROM "idea3_stop" U0
            WHERE U0."station_name" = Station 3
        )
        AND (
            SELECT U0."arrival_time"
            FROM "idea3_stop" U0
            WHERE (
                    U0."station_name" = Station 1
                    AND U0."train_id" = ("idea3_train"."id")
                )
            LIMIT 1
        ) < (
            SELECT U0."arrival_time"
            FROM "idea3_stop" U0
            WHERE (
                    U0."station_name" = Station 3
                    AND U0."train_id" = ("idea3_train"."id")
                )
            LIMIT 1
        )
    )