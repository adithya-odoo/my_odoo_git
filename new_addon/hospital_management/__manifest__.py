{
    'name' : 'Hospital Management',
    'description' : 'Hospital management',
    'application': True,
    'depends':[
        'base',
        'hr'
    ],

    'data' :[
        'views/hospital_doctor.xml',
        'views/hospital_department.xml',
        'views/op_ticket.xml',
        'views/hospital_consultation.xml',
        'views/hospital_patient.xml',
        'security/ir.models.access.csv'
    ]
}