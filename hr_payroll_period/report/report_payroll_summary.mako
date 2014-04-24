<html>
<head>
    <style type="text/css">
        ${css}
    </style>
</head>
<body>
    <br/>
    <br/>
    <br/>
    <center><h2><u>${("Payroll Summary")}</u></h2></center>
    <br/>
    <br/>
    <table class="concept_table" width="100%">
        <thead>
            <tr>
                <th style="text-align:center;"></th>
                <th style="text-align:left;">${_("Identification No")}</th>
                <th style="text-align:left;">${_("Employee")}</th>
                <th style="text-align:left;">${_("Designation")}</th>
                <th style="text-align:right;">${_("Allocation")}</th>
                <th style="text-align:right;" >${_("Deduction")}</th>
                <th style="text-align:right;" >${_("Net")}</th>
            </tr>
        </thead>
        <tbody>
            %for o in objects:
                <tr>
                    <td>${helper.embed_image('png',o.employee_id.image_small)|n }</td>
                    <td>${o.employee_id.identification_id or ''|entity}</td>
                    <td>${o.employee_id.name or ''|entity}</td>
                    <td>${o.employee_id.job_id.name or ''|entity}</td>                    
                    <td style="text-align:right;">${formatLang(get_allocation_total(o.line_ids))}</td>
                    <td style="text-align:right;">${formatLang(get_deduction_total(o.line_ids))}</td>
                    <td style="text-align:right;">${formatLang(get_total_net(o.line_ids))}</td>
                </tr>
            %endfor
        </tbody>
    </table>
</body>