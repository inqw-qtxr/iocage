# Copyright (c) 2014-2019, iocage
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted providing that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
# IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import pytest


require_root = pytest.mark.require_root
require_zpool = pytest.mark.require_zpool


SORTING_FLAGS = ['name', 'created', 'rsize', 'used']


def common_function(
    invoke_cli, jail, parse_rows_output,
    jails_as_rows, full=False
):
    for flag in SORTING_FLAGS:
        if isinstance(jail, list):
            command = ['snaplist', 'ALL', '-s', flag]
        else:
            command = ['snaplist', jail.name, '-s', flag]
        if full:
            command.append('-l')

        result = invoke_cli(
            command
        )

        if isinstance(jail, list):
            jails = jail
            orig_list = parse_rows_output(result.output, 'snapall')
            verify_list = []
            for jail in jails:
                for row in jails_as_rows(jail.recursive_snapshots, full=full):
                    row.jail = jail.name
                    verify_list.append(row)
        else:
            orig_list = parse_rows_output(result.output, 'snapshot')
            verify_list = jails_as_rows(jail.recursive_snapshots, full=full)

        verify_list.sort(key=lambda r: r.sort_flag(flag))

        assert verify_list == orig_list


@require_root
@require_zpool
def test_01_list_snapshots_of_jail(
    invoke_cli, resource_selector, skip_test,
    parse_rows_output, jails_as_rows
):
    jails = resource_selector.jails_having_snapshots
    skip_test(not jails)

    common_function(invoke_cli, jails[0], parse_rows_output, jails_as_rows)


@require_root
@require_zpool
def test_02_list_snapshots_of_template_jail(
    invoke_cli, resource_selector, skip_test,
    parse_rows_output, jails_as_rows
):
    jails = resource_selector.templates_having_snapshots
    skip_test(not jails)

    common_function(invoke_cli, jails[0], parse_rows_output, jails_as_rows)


@require_root
@require_zpool
def test_03_list_snapshots_of_jail_with_long_flag(
    invoke_cli, resource_selector, skip_test,
    parse_rows_output, jails_as_rows
):
    jails = resource_selector.all_jails_having_snapshots
    skip_test(not jails)

    common_function(
        invoke_cli, jails[0], parse_rows_output, jails_as_rows, True
    )


@require_root
@require_zpool
def test_04_list_snapshots_of_all_jails(
    invoke_cli, resource_selector, skip_test,
    parse_rows_output, jails_as_rows
):
    jails = resource_selector.all_jails_having_snapshots
    skip_test(not jails)

    common_function(
        invoke_cli, jails, parse_rows_output, jails_as_rows
    )


@require_root
@require_zpool
def test_05_list_snapshots_of_all_jails_with_long_flag(
    invoke_cli, resource_selector, skip_test,
    parse_rows_output, jails_as_rows
):
    jails = resource_selector.all_jails_having_snapshots
    skip_test(not jails)

    common_function(
        invoke_cli, jails, parse_rows_output, jails_as_rows, True
    )
