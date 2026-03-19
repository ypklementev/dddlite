import xlsxwriter


class ExcelWriter:
    def write_streaming(self, filepath: str, analyzer):
        workbook = xlsxwriter.Workbook(
            filepath,
            {"constant_memory": True}
        )

        sheet = workbook.add_worksheet()
        sheet.write_row(0, 0, ["Словоформа", "Всего", "По строкам"])

        row = 1

        for lemma, total in analyzer.global_count.items():
            line_map = analyzer.line_counts.get(lemma, {})

            max_line = max(line_map.keys(), default=-1)

            # формируем строку без хранения всего списка
            parts = []
            for i in range(max_line + 1):
                parts.append(str(line_map.get(i, 0)))

            per_line_str = ",".join(parts)

            sheet.write_row(row, 0, [lemma, total, per_line_str])
            row += 1

        workbook.close()