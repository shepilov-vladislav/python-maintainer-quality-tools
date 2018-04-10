from collections import defaultdict

from . import color_helpers

from .text import ColorizedTextFormatter

__all__ = ('ColorizedGroupedFormatter', )


class ColorizedGroupedFormatter(ColorizedTextFormatter):

    def render_messages(self):
        output = [
            'Messages',
            '========',
            '',
        ]

        # pylint: disable=unnecessary-lambda
        groups = defaultdict(lambda: defaultdict(list))

        for message in self.messages:
            groups[message.location.path][message.location.line].append(message)

        for filename in sorted(groups.keys()):
            output.append(color_helpers.yellow(filename))

            for line in sorted(
                groups[filename].keys(),
                key=lambda x: 0 if x is None else int(x)
            ):
                output.append(color_helpers.yellow_light('  Line: %s' % line))

                for message in groups[filename][line]:
                    output.append(
                        '    %s: %s / %s%s' % (
                            color_helpers.bright_magenta(message.source),
                            color_helpers.bright_blue(message.code),
                            message.message,
                            (' (col %s)' % message.location.character)
                            if message.location.character else '',
                        )
                    )

            output.append('')

        return '\n'.join(output)
