from keeper import error


class Keeper:
    def __init__(self, frame_engine, vehicles_engine):
        self.fe = frame_engine
        self.ve = vehicles_engine

    async def serve(self, data):
        try:
            for f in self.fe.get_frames(data):
                # Регистрируем транспорт если он не зарегистрирован.
                # Возвращаем ссылку на зарегистрированный транспорт
                vehicle = self.ve.produce(f)

                if vehicle.route_detected:
                    # только для ТС с определенным маршрутом
                    # можно проверять маршрут и остановки
                    await vehicle.check_speed()
                    await vehicle.check_route()
                    await vehicle.check_direction()
                else:
                    # иначе пытаемся определить маршрут
                    await vehicle.detect_route()

            await self.ve.garbage_collector()

        except error.KeeperFrameTypeError:
            pass
        except error.KeeperError:
            pass
